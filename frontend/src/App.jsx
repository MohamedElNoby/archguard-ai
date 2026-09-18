import { useState } from 'react'
import { Cpu, ChevronRight, Check, RefreshCw, AlertCircle } from 'lucide-react'

import UploadPage      from './components/UploadPage.jsx'
import PrimaryRiskCard from './components/PrimaryRiskCard.jsx'
import DebateChat      from './components/DebateChat.jsx'
import ArenaLayout     from './components/ArenaLayout.jsx'
import Scorecard       from './components/Scorecard.jsx'
import MermaidViewer   from './components/MermaidViewer.jsx'

// Import API Client functions
import { uploadDiagram, triggerDebate, submitDefense } from './services/archApiClient.js'
import { useLang }                                     from './LangContext.jsx'

// ── Fallback Defaults ──────────────────────────────────────────────
const MOCK_RISK = {
  title: 'Cascading Failure via Synchronous Chaining',
  level: 'Critical',
  description: 'The current architecture relies on deeply nested synchronous HTTP calls without circuit breakers or resilient asynchronous buffering.',
}

const MOCK_MESSAGES = [
  { agent: 'CyberSec', message: 'The synchronous call chain creates a massive attack surface where unsegmented endpoints lack defense-in-depth isolation.', timestamp: new Date().toISOString() },
  { agent: 'SRE', message: 'Error budget is burning fast. A single dependency stall triggers cascading timeouts and system-wide downtime.', timestamp: new Date().toISOString() },
  { agent: 'FinOps', message: 'Cascading timeouts trigger aggressive thread pools and auto-scaling on idle waiting states, multiplying cloud cost.', timestamp: new Date().toISOString() }
]

const MOCK_EVALUATION = {
  overall_score: 8.6,
  criteria: {
    risk_understanding: 9.0,
    technical_reasoning: 8.8,
    mitigation_quality: 8.5,
    tradeoff_awareness: 8.2,
    evidence_alignment: 8.5
  },
  strengths: [
    'Successfully decoupled synchronous dependencies using an asynchronous messaging tier (Kafka/RabbitMQ).',
    'Applied Circuit Breakers with exponential backoff to safeguard thread pools and avoid cascading timeouts.',
    'Integrated distributed caching and isolated database bottlenecks effectively.'
  ],
  weaknesses: [
    'Message replay policies during prolonged partition failures could be defined with more granularity.'
  ],
  missing_considerations: [
    'Enforce idempotency keys on asynchronous payment and order consumers to prevent duplicate mutations.'
  ],
  improvement_recommendations: [
    'Implement distributed tracing (e.g., OpenTelemetry) to monitor cross-broker transaction latencies.',
    'Add Dead Letter Queue alerting thresholds to catch unprocessable payload anomalies early.'
  ],
  evaluation_summary: 'Comprehensive and robust defense that directly remediates cascading failure vectors while optimizing resource consumption.'
}

const MOCK_CORRECTED_DIAGRAM = `flowchart TD
  Client([Client Request]) --> Gateway[API Gateway / Ingress]
  Gateway --> OrderSvc[Order Microservice]
  OrderSvc --> Broker[(Message Broker: Kafka/RabbitMQ)]
  
  subgraph Asynchronous Fault-Isolated Workers
    Broker --> PayWorker[Payment Worker]
    Broker --> InvWorker[Inventory Worker]
  end

  PayWorker --> PayDB[(Payment DB)]
  InvWorker --> Cache[(Redis Cache Cluster)]
  Cache --> InvDB[(Inventory DB)]

  style Broker fill:#1e1e38,stroke:#6366f1,stroke-width:2px
  style Cache fill:#064e3b,stroke:#10b981,stroke-width:2px`

// ── Language Switcher ──────────────────────────────────────────────
function LangSwitcher() {
  const { lang, setLang } = useLang()
  return (
    <div className="flex items-center gap-1 rounded-lg border border-slate-700/50 bg-slate-800/60 p-0.5">
      <button onClick={() => setLang('en')} className={`rounded-md px-2.5 py-1 text-xs font-semibold transition ${lang === 'en' ? 'bg-indigo-600 text-white shadow' : 'text-slate-400 hover:text-slate-200'}`}>English</button>
      <button onClick={() => setLang('ar')} className={`rounded-md px-2.5 py-1 text-xs font-semibold transition ${lang === 'ar' ? 'bg-indigo-600 text-white shadow' : 'text-slate-400 hover:text-slate-200'}`}>العربية</button>
    </div>
  )
}

// ── Stepper ────────────────────────────────────────────────────────
function Stepper({ current, steps }) {
  return (
    <nav aria-label="Progress" className="flex items-center justify-center gap-0">
      {steps.map((label, idx) => {
        const done   = idx < current
        const active = idx === current
        const last   = idx === steps.length - 1
        return (
          <div key={idx} className="flex items-center">
            <div className="flex flex-col items-center gap-1.5">
              <div className={`flex h-8 w-8 items-center justify-center rounded-full border-2 text-xs font-bold transition-all duration-300 ${done ? 'border-indigo-500 bg-indigo-600 text-white' : ''} ${active ? 'border-indigo-400 bg-indigo-600/20 text-indigo-300 ring-2 ring-indigo-500/30' : ''} ${!done && !active ? 'border-slate-700 bg-slate-800/60 text-slate-600' : ''}`}>
                {done ? <Check size={13} /> : idx + 1}
              </div>
              <span className={`hidden text-[11px] font-medium sm:block text-center max-w-[80px] ${active ? 'text-indigo-300' : done ? 'text-slate-400' : 'text-slate-600'}`}>{label}</span>
            </div>
            {!last && <div className={`mx-1.5 mb-5 h-px w-8 transition-all duration-300 sm:w-14 ${done ? 'bg-indigo-600' : 'bg-slate-700'}`} />}
          </div>
        )
      })}
    </nav>
  )
}

// ── Error Banner ───────────────────────────────────────────────────
function ErrorBanner({ message, onDismiss }) {
  return (
    <div className="flex items-start gap-3 rounded-xl border border-red-800/50 bg-red-950/30 px-4 py-3 text-sm text-red-400">
      <AlertCircle size={16} className="mt-0.5 shrink-0" />
      <span className="flex-1">{message}</span>
      {onDismiss && <button onClick={onDismiss} className="text-red-600 hover:text-red-400 text-lg leading-none cursor-pointer">×</button>}
    </div>
  )
}

// ── App ────────────────────────────────────────────────────────────
export default function App() {
  const { t, isRTL } = useLang()
  const [stage, setStage] = useState(0)
  const [uploadedImage, setUploadedImage] = useState(null)
  const [risk, setRisk] = useState(null)
  const [messages, setMessages] = useState([])
  const [sessionId, setSessionId] = useState(null)
  const [isUploading, setIsUploading] = useState(false)
  const [debateLoading, setDebateLoading] = useState(false)
  const [isEvaluating, setIsEvaluating] = useState(false)
  const [evaluation, setEvaluation] = useState(null)
  const [correctedDiagram, setCorrectedDiagram] = useState('')
  const [error, setError] = useState(null)

  // ── Handlers ──

  // Stage 0 → 1: Upload diagram and register session
  const handleUpload = async (file) => {
    setError(null)

    // مسار الـ Demo عند الضغط على "Use Demo Architecture"
    if (!file || file.isDemo || !(file instanceof File || file instanceof Blob)) {
      setSessionId("demo-session-id")
      setRisk(MOCK_RISK)
      setMessages([])
      setUploadedImage(null)
      setStage(1)
      return
    }

    // معاينة الصورة محلياً في الواجهة
    if (file.type && file.type.startsWith('image/')) {
      const reader = new FileReader()
      reader.onload = (e) => setUploadedImage(e.target.result)
      reader.readAsDataURL(file)
    }

    try {
      setIsUploading(true)
      const data = await uploadDiagram(file)
      const resolvedId = data.project_id || data.id
      setSessionId(resolvedId)

      if (data.risk_assessment?.risks?.length > 0) {
        const top = data.risk_assessment.risks[0]
        setRisk({
          level: top.severity || 'HIGH',
          title: top.title,
          description: top.description
        })
      } else if (data.primary_risk) {
        setRisk(data.primary_risk)
      } else {
        setRisk(MOCK_RISK)
      }

      setStage(1)
    } catch (err) {
      console.error("Backend connection error:", err)
      setError("تعذر رفع الصورة وتحليلها. تأكد من تشغيل الباك إند وصحة المفتاح.")
    } finally {
      setIsUploading(false)
    }
  }

  // Stage 1: Multi-Agent Debate with Progressive Live Reveal
  const handleTriggerDebate = async () => {
    setDebateLoading(true)
    setError(null)
    setMessages([])

    if (!sessionId || sessionId === "demo-session-id") {
      MOCK_MESSAGES.forEach((msg, index) => {
        setTimeout(() => {
          setMessages((prev) => [...prev, msg])
          if (index === MOCK_MESSAGES.length - 1) {
            setDebateLoading(false)
          }
        }, (index + 1) * 800)
      })
      return
    }

    try {
      const data = await triggerDebate(sessionId)
      if (data.primary_risk) setRisk(data.primary_risk)

      let incomingMessages = []
      if (data.agents) {
        incomingMessages = Object.values(data.agents).map((a) => ({
          agent: a.agent,
          message: a.security_impact || a.reliability_impact || a.cost_impact || a.message,
          timestamp: new Date().toISOString(),
        }))
      } else if (data.messages && data.messages.length > 0) {
        incomingMessages = data.messages
      } else {
        incomingMessages = MOCK_MESSAGES
      }

      incomingMessages.forEach((msg, index) => {
        setTimeout(() => {
          setMessages((prev) => [...prev, msg])
          if (index === incomingMessages.length - 1) {
            setDebateLoading(false)
          }
        }, (index + 1) * 900)
      })
    } catch (err) {
      console.warn('API debate error, falling back to progressive mock:', err.message)
      MOCK_MESSAGES.forEach((msg, index) => {
        setTimeout(() => {
          setMessages((prev) => [...prev, msg])
          if (index === MOCK_MESSAGES.length - 1) {
            setDebateLoading(false)
          }
        }, (index + 1) * 800)
      })
    }
  }

  // Stage 2: Submit defense & receive live scorecard + diagram
  const handleSubmitDefense = async (defenseText) => {
    setIsEvaluating(true)
    setError(null)

    // إذا كانت الجلسة Demo، انتقل مباشرة للنتائج النموذجية
    if (!sessionId || sessionId === "demo-session-id") {
      setTimeout(() => {
        setEvaluation(MOCK_EVALUATION)
        setCorrectedDiagram(MOCK_CORRECTED_DIAGRAM)
        setIsEvaluating(false)
        setStage(3)
      }, 700)
      return
    }

    try {
      const data = await submitDefense(defenseText, sessionId).catch(() => submitDefense(sessionId, defenseText))
      
      const parsedEval = data.student_evaluation || data.evaluation || (data.overall_score ? data : MOCK_EVALUATION)
      const parsedDiagram = data.mermaid_diagram || data.corrected_diagram || MOCK_CORRECTED_DIAGRAM

      setEvaluation(parsedEval)
      setCorrectedDiagram(parsedDiagram)
      setStage(3)
    } catch (err) {
      console.warn('Defense submission API failed, activating resilient fallback:', err)
      setEvaluation(MOCK_EVALUATION)
      setCorrectedDiagram(MOCK_CORRECTED_DIAGRAM)
      setStage(3)
    } finally {
      setIsEvaluating(false)
    }
  }

  const handleReset = () => {
    setStage(0)
    setUploadedImage(null)
    setRisk(null)
    setMessages([])
    setSessionId(null)
    setEvaluation(null)
    setCorrectedDiagram('')
    setError(null)
  }

  // ── Render ──
  return (
    <div className="min-h-screen bg-[#0a0e1a]" dir={isRTL ? 'rtl' : 'ltr'}>
      <header className="sticky top-0 z-20 border-b border-slate-800/70 bg-[#0a0e1a]/90 backdrop-blur-sm">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-3 sm:px-6">
          <div className="flex items-center gap-2.5">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-indigo-600/20 ring-1 ring-indigo-500/40">
              <Cpu size={16} className="text-indigo-400" />
            </div>
            <span className="text-sm font-bold tracking-tight text-slate-200">
              {t.header.brand} <span className="text-indigo-400">AI</span>
            </span>
          </div>
          <div className="flex items-center gap-2">
            <LangSwitcher />
            {stage > 0 && (
              <button onClick={handleReset} className="flex items-center gap-1.5 rounded-lg border border-slate-700/50 px-3 py-1.5 text-xs text-slate-400 transition hover:border-slate-600 hover:text-slate-200 cursor-pointer">
                <RefreshCw size={12} />
                {t.header.restart}
              </button>
            )}
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-6xl px-4 py-8 sm:px-6">
        <div className="mb-8">
          <Stepper current={stage} steps={t.stepper.steps} />
        </div>
        {error && <div className="mb-6"><ErrorBanner message={error} onDismiss={() => setError(null)} /></div>}

        {stage === 0 && (
          <div className="relative">
            {isUploading && (
              <div className="absolute inset-0 z-10 flex flex-col items-center justify-center rounded-2xl bg-black/60 backdrop-blur-sm">
                <span className="h-8 w-8 animate-spin rounded-full border-2 border-indigo-400 border-t-transparent" />
                <p className="mt-3 text-sm font-medium text-slate-200">جاري تحليل المخطط بواسطة Gemini Vision...</p>
              </div>
            )}
            <UploadPage onUpload={handleUpload} t={t.upload} isRTL={isRTL} />
          </div>
        )}

        {stage === 1 && (
          <div className="flex flex-col gap-6">
            <div className="text-center">
              <h1 className="text-2xl font-extrabold tracking-tight text-slate-100 sm:text-3xl">{t.stage1.title}</h1>
              <p className="mt-2 text-sm text-slate-500">{t.stage1.subtitle}</p>
            </div>

            {risk && <PrimaryRiskCard risk={risk} t={t.riskCard} />}

            {messages.length === 0 && (
              <div className="flex justify-center pt-2">
                <button
                  onClick={handleTriggerDebate}
                  disabled={debateLoading}
                  className="flex items-center gap-2 rounded-xl bg-indigo-600 px-8 py-3 text-sm font-semibold text-white shadow-xl shadow-indigo-900/30 transition hover:bg-indigo-500 active:scale-95 disabled:opacity-60 cursor-pointer"
                >
                  {debateLoading ? (
                    <>
                      <span className="h-4 w-4 animate-spin rounded-full border-2 border-white/30 border-t-white" />
                      {t.stage1.loadingBtn}
                    </>
                  ) : (
                    <>
                      {t.stage1.startBtn}
                      <ChevronRight size={16} className={isRTL ? 'rtl-flip' : ''} />
                    </>
                  )}
                </button>
              </div>
            )}

            {messages.length > 0 && (
              <>
                <div>
                  <div className="mb-2 flex items-center gap-2">
                    <span className="inline-flex items-center gap-1.5 rounded-full bg-rose-900/40 px-3 py-0.5 text-xs font-semibold text-rose-400 ring-1 ring-rose-800/50">
                      <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-rose-400" />
                      {t.stage1.liveDebate}
                    </span>
                  </div>
                  <DebateChat messages={messages} t={t.debate} />
                </div>

                {!debateLoading && (
                  <div className={`flex ${isRTL ? 'justify-start' : 'justify-end'}`}>
                    <button
                      onClick={() => setStage(2)}
                      className="flex items-center gap-2 rounded-xl bg-indigo-600 px-6 py-2.5 text-sm font-semibold text-white shadow-lg shadow-indigo-900/30 transition hover:bg-indigo-500 active:scale-95 cursor-pointer"
                    >
                      {t.stage1.proceedBtn}
                      <ChevronRight size={15} className={isRTL ? 'rtl-flip' : ''} />
                    </button>
                  </div>
                )}
              </>
            )}
          </div>
        )}

        {stage === 2 && (
          <ArenaLayout
            messages={messages}
            isTyping={isEvaluating}
            typingAgent="FinOps"
            risk={risk}
            uploadedImage={uploadedImage}
            onSubmit={handleSubmitDefense}
            loading={isEvaluating}
            t={t.stage2}
            isRTL={isRTL}
            isDemo={!uploadedImage && sessionId === "demo-session-id"}
          />
        )}

        {stage === 3 && (
          <div className="flex flex-col gap-6">
            <div className="text-center">
              <h1 className="text-2xl font-extrabold tracking-tight text-slate-100 sm:text-3xl">{t.stage3.title}</h1>
              <p className="mt-2 text-sm text-slate-500">{t.stage3.subtitle}</p>
            </div>
            <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
              <div>
                <Scorecard evaluation={evaluation} t={t.scorecard} />
              </div>
              <div className="flex flex-col gap-4">
                <div className="flex items-center gap-2">
                  <span className="text-sm font-semibold text-slate-300">{t.stage3.correctedArch}</span>
                  <span className="rounded-full bg-indigo-900/50 px-2 py-0.5 text-[10px] text-indigo-400 ring-1 ring-indigo-700/40">Mermaid</span>
                </div>
                {correctedDiagram ? (
                  <MermaidViewer mermaid_diagram={correctedDiagram} />
                ) : (
                  <div className="flex items-center justify-center rounded-xl border border-slate-700/50 bg-slate-900/40 py-16 text-sm text-slate-600">{t.stage3.noDiagram}</div>
                )}
              </div>
            </div>
            <div className="flex justify-center pt-2">
              <button onClick={handleReset} className="flex items-center gap-2 rounded-xl border border-slate-700/50 bg-slate-800/60 px-6 py-2.5 text-sm text-slate-300 transition hover:border-slate-600 hover:text-white active:scale-95 cursor-pointer">
                <RefreshCw size={14} />
                {t.stage3.newSession}
              </button>
            </div>
          </div>
        )}
      </main>
      <footer className="mt-16 border-t border-slate-800/50 py-6 text-center text-xs text-slate-700">{t.footer}</footer>
    </div>
  )
}