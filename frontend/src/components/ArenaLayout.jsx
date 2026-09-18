import { useState, useRef, useEffect } from 'react'
import { Shield, Activity, Wallet, Send, Loader2, Sparkles } from 'lucide-react'

// ── Constants ─────────────────────────────────────────────────────────────

const MAX_CHARS = 500

const DEMO_DEFENSE_TEXT =
  "To resolve the cascading failure, we break synchronous chaining by placing an asynchronous message queue (e.g., Kafka/RabbitMQ) between Order and downstream services. We apply Circuit Breaker and Retry patterns with exponential backoff on HTTP calls, backed by Redis caching and Dead Letter Queues (DLQ) to isolate faults without consuming idle thread resources."

const AGENT_CFG = {
  CyberSec: {
    icon: Shield,
    avatar: '🧑‍💻',
    border:     'border-red-700/60',
    bg:         'bg-red-950/40',
    headerBg:   'bg-red-950/60',
    badge:      'bg-red-900/70 text-red-300',
    iconColor:  'text-red-400',
    ring:       'ring-red-700/40',
    dot:        'bg-red-500',
    msgBorder:  'border-red-800/40',
    msgBg:      'bg-red-950/30',
  },
  SRE: {
    icon: Activity,
    avatar: '👨‍🔧',
    border:     'border-blue-700/60',
    bg:         'bg-blue-950/40',
    headerBg:   'bg-blue-950/60',
    badge:      'bg-blue-900/70 text-blue-300',
    iconColor:  'text-blue-400',
    ring:       'ring-blue-700/40',
    dot:        'bg-blue-400',
    msgBorder:  'border-blue-800/40',
    msgBg:      'bg-blue-950/30',
  },
  FinOps: {
    icon: Wallet,
    avatar: '💼',
    border:     'border-emerald-700/60',
    bg:         'bg-emerald-950/40',
    headerBg:   'bg-emerald-950/60',
    badge:      'bg-emerald-900/70 text-emerald-300',
    iconColor:  'text-emerald-400',
    ring:       'ring-emerald-700/40',
    dot:        'bg-emerald-400',
    msgBorder:  'border-emerald-800/40',
    msgBg:      'bg-emerald-950/30',
  },
}

// ── Agent Presence Card (top of right panel) ──────────────────────────────

function AgentCard({ agentKey, status }) {
  const cfg  = AGENT_CFG[agentKey]
  const Icon = cfg.icon
  return (
    <div className={`flex flex-1 flex-col gap-1.5 rounded-xl border ${cfg.border} ${cfg.bg} px-3 py-2.5 min-w-0`}>
      {/* Name row */}
      <div className="flex items-center gap-2">
        <div className={`flex h-7 w-7 shrink-0 items-center justify-center rounded-full text-base leading-none ring-1 ${cfg.ring} bg-slate-800`}>
          {cfg.avatar}
        </div>
        <span className={`text-xs font-bold ${cfg.iconColor} truncate`}>{status.role}</span>
      </div>
      {/* Status */}
      <div className="flex items-center gap-1.5">
        <span className={`h-1.5 w-1.5 shrink-0 rounded-full ${cfg.dot} animate-pulse`} />
        <span className="text-[11px] font-semibold text-slate-300 truncate">{status.status}</span>
      </div>
      {/* Focus */}
      <p className="text-[10px] text-slate-500 leading-snug">{status.focus}</p>
    </div>
  )
}

// ── Message bubble ────────────────────────────────────────────────────────

function MessageBubble({ msg }) {
  const cfg  = AGENT_CFG[msg.agent] ?? AGENT_CFG.SRE
  const Icon = cfg.icon
  return (
    <div className={`msg-enter flex items-start gap-3 rounded-xl border p-3 ${cfg.msgBg} ${cfg.msgBorder}`}>
      {/* Avatar */}
      <div className={`mt-0.5 shrink-0 flex h-7 w-7 items-center justify-center rounded-full ring-1 ${cfg.ring} bg-slate-800 text-sm leading-none`}>
        {cfg.avatar}
      </div>
      {/* Body */}
      <div className="flex min-w-0 flex-1 flex-col gap-0.5">
        <div className="flex items-center justify-between gap-2">
          <span className={`text-[11px] font-bold ${cfg.iconColor}`}>{msg.agent}</span>
          {msg.timestamp && (
            <span className="shrink-0 text-[10px] text-slate-600">
              {new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
            </span>
          )}
        </div>
        <p className="text-sm leading-relaxed text-slate-300 break-words">{msg.message}</p>
      </div>
      {/* Agent icon badge */}
      <div className={`mt-0.5 shrink-0 rounded-md p-1 ${cfg.badge}`}>
        <Icon size={11} className={cfg.iconColor} />
      </div>
    </div>
  )
}

// ── Typing indicator bubble ───────────────────────────────────────────────

function TypingBubble({ agentKey }) {
  const cfg  = AGENT_CFG[agentKey] ?? AGENT_CFG.SRE
  return (
    <div className={`msg-enter flex items-center gap-3 rounded-xl border p-3 ${cfg.msgBg} ${cfg.msgBorder}`}>
      <div className={`shrink-0 flex h-7 w-7 items-center justify-center rounded-full ring-1 ${cfg.ring} bg-slate-800 text-sm leading-none`}>
        {cfg.avatar}
      </div>
      <span className={`text-[11px] font-bold ${cfg.iconColor} me-1`}>{agentKey}</span>
      <span className="text-xs text-slate-400">is typing…</span>
      <div className="flex gap-1">
        <span className="typing-dot h-1.5 w-1.5 rounded-full bg-slate-400" />
        <span className="typing-dot h-1.5 w-1.5 rounded-full bg-slate-400" />
        <span className="typing-dot h-1.5 w-1.5 rounded-full bg-slate-400" />
      </div>
    </div>
  )
}

// ── Left Panel — Architecture Recap ──────────────────────────────────────

function RecapPanel({ uploadedImage, risk, t }) {
  return (
    <div className="flex h-full flex-col gap-4 rounded-2xl border border-slate-700/50 bg-[#0d1424] p-4">
      {/* Title */}
      <h2 className="text-sm font-bold text-slate-200">{t.recapTitle}</h2>

      {/* Architecture thumbnail */}
      <div className="flex-1 overflow-hidden rounded-xl border border-slate-700/40 bg-slate-900/60 flex items-center justify-center min-h-[160px] p-2">
        {uploadedImage ? (
          <img
            src={uploadedImage}
            alt="Architecture diagram"
            className="h-full w-full object-contain"
          />
        ) : (
          /* Demo architecture: Clear Synchronous Chain Representation */
          <div className="flex flex-col items-center gap-1.5 py-2 px-1 w-full">
            <div className="w-full text-center py-1 px-2 rounded border border-indigo-500/40 bg-indigo-950/40 text-[10px] font-mono text-indigo-300">
              Client Request (HTTP)
            </div>
            <div className="text-slate-500 text-[10px] leading-none">↓ sync</div>

            <div className="w-full text-center py-1 px-2 rounded border border-rose-500/50 bg-rose-950/40 text-[10px] font-mono text-rose-300">
              Order Gateway
            </div>
            <div className="text-slate-500 text-[10px] leading-none">↓ blocking call</div>

            <div className="w-full text-center py-1 px-2 rounded border border-amber-500/50 bg-amber-950/40 text-[10px] font-mono text-amber-300">
              Payment Service
            </div>
            <div className="text-slate-500 text-[10px] leading-none">↓ blocking call</div>

            <div className="w-full text-center py-1 px-2 rounded border border-red-600/70 bg-red-950/60 text-[10px] font-mono text-red-400">
              Inventory DB (Stall)
            </div>

            <span className="mt-2 text-[9px] text-rose-400/90 font-medium text-center leading-tight">
              ⚠️ Cascading failure: No buffer or circuit breaker
            </span>
          </div>
        )}
      </div>

      {/* Caption */}
      <p className="text-[11px] text-slate-500 leading-snug">{t.recapDesc}</p>

      {/* Discovered risks */}
      {risk && (
        <div>
          <p className="mb-1.5 text-[11px] font-bold text-slate-400">{t.discoveredRisks}</p>
          <ul className="flex flex-col gap-1">
            <li className="flex items-center gap-1.5 text-[11px]">
              <span className="text-red-400 font-semibold truncate">{risk.title}</span>
              <span className="shrink-0 rounded-full bg-red-900/60 px-1.5 py-0.5 text-[9px] font-bold text-red-300 uppercase">
                {risk.level} 🔴
              </span>
            </li>
          </ul>
        </div>
      )}
    </div>
  )
}

// ── Main Component ────────────────────────────────────────────────────────

export default function ArenaLayout({
  messages      = [],
  isTyping      = false,
  typingAgent   = 'FinOps',
  risk          = null,
  uploadedImage = null,
  onSubmit,
  loading       = false,
  t,
  isRTL         = false,
  isDemo        = false,
}) {
  const [text, setText] = useState('')
  const bottomRef = useRef(null)
  const remaining = MAX_CHARS - text.length

  // auto-scroll on new messages
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isTyping])

  const handleSubmit = () => {
    const trimmed = text.trim()
    if (!trimmed || loading || remaining < 0) return
    onSubmit(trimmed)
  }

  const handleKeyDown = (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
      e.preventDefault()
      handleSubmit()
    }
  }

  const handleFillDemo = () => {
    setText(DEMO_DEFENSE_TEXT.slice(0, MAX_CHARS))
  }

  return (
    <div className="flex flex-col gap-4">
      {/* Page title */}
      <div>
        <h1 className="text-xl font-extrabold tracking-tight text-slate-100 sm:text-2xl">
          {t.title}
        </h1>
        <p className="mt-1 text-xs text-slate-500">{t.subtitle}</p>
      </div>

      {/* ── Two-column arena ── */}
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-[240px_1fr]">

        {/* ── LEFT: Architecture Recap ── */}
        <RecapPanel uploadedImage={uploadedImage} risk={risk} t={t} />

        {/* ── RIGHT: Jury panel ── */}
        <div className="flex flex-col gap-3">

          {/* Agent presence row */}
          <div className="flex gap-2 flex-wrap sm:flex-nowrap">
            {['CyberSec', 'SRE', 'FinOps'].map((key) => (
              <AgentCard key={key} agentKey={key} status={t.agentStatus[key]} />
            ))}
          </div>

          {/* Jury Debate panel */}
          <div className="rounded-2xl border border-slate-700/50 bg-[#0d1424]">
            {/* Panel header */}
            <div className="border-b border-slate-700/50 px-4 py-2.5">
              <span className="text-sm font-bold text-slate-200">{t.juryDebateTitle}</span>
            </div>

            {/* Messages scroll area */}
            <div className="flex max-h-[320px] flex-col gap-2 overflow-y-auto p-3 md:max-h-[360px]">
              {messages.length === 0 && !isTyping ? (
                <div className="flex flex-col items-center justify-center py-10 text-center text-slate-600">
                  <Activity size={28} className="mb-2 opacity-40" />
                  <p className="text-sm">{t.juryDebateTitle}…</p>
                </div>
              ) : (
                <>
                  {messages.map((msg, i) => (
                    <MessageBubble key={i} msg={msg} />
                  ))}
                  {isTyping && <TypingBubble agentKey={typingAgent} />}
                </>
              )}
              <div ref={bottomRef} />
            </div>
          </div>

          {/* ── Adversarial Challenge input bar ── */}
          <div className="rounded-2xl border-2 border-yellow-600/60 bg-[#0d1424] overflow-hidden">
            {/* Hazard header */}
            <div className="flex items-center justify-between bg-yellow-500/10 px-4 py-2 border-b border-yellow-600/40">
              <div className="flex items-center gap-2">
                <div className="flex gap-0.5">
                  {[...Array(4)].map((_, i) => (
                    <div
                      key={i}
                      className="h-4 w-2.5 rotate-12 rounded-sm"
                      style={{ background: i % 2 === 0 ? '#ca8a04' : '#0d1424' }}
                    />
                  ))}
                </div>
                <span className="text-xs font-extrabold tracking-widest text-yellow-400 uppercase">
                  {t.challengeLabel}
                </span>
              </div>

              {/* Demo Fill Button (Only visible in Demo Mode) */}
              {isDemo && (
                <button
                  type="button"
                  onClick={handleFillDemo}
                  disabled={loading}
                  className="flex items-center gap-1.5 rounded-lg border border-yellow-500/40 bg-yellow-500/10 px-2.5 py-1 text-[11px] font-semibold text-yellow-300 transition hover:bg-yellow-500/20 active:scale-95 disabled:opacity-50 cursor-pointer"
                >
                  <Sparkles size={12} />
                  <span>Fill Demo Defense</span>
                </button>
              )}
            </div>

            {/* Text input area */}
            <div className="p-3">
              <textarea
                value={text}
                onChange={(e) => setText(e.target.value.slice(0, MAX_CHARS + 20))}
                onKeyDown={handleKeyDown}
                disabled={loading}
                placeholder={t.placeholder}
                rows={3}
                className="w-full resize-none rounded-lg border border-slate-700/60 bg-slate-800/60 px-3 py-2.5 text-sm text-slate-200 placeholder-slate-600 outline-none transition focus:border-indigo-600/60 focus:ring-1 focus:ring-indigo-600/30 disabled:opacity-50"
              />

              {/* Footer row: char count + submit */}
              <div className="mt-2 flex items-center justify-between gap-3">
                <span className={`text-xs ${remaining < 50 ? 'text-red-400' : 'text-slate-500'}`}>
                  {Math.max(remaining, 0)} / {MAX_CHARS} {t.charsRemaining}
                </span>

                <button
                  onClick={handleSubmit}
                  disabled={loading || !text.trim() || remaining < 0}
                  className="flex items-center gap-2 rounded-xl bg-emerald-600 px-5 py-2 text-sm font-bold text-white shadow-lg shadow-emerald-900/30 transition hover:bg-emerald-500 active:scale-95 disabled:cursor-not-allowed disabled:opacity-50 cursor-pointer"
                >
                  {loading ? (
                    <>
                      <Loader2 size={14} className="animate-spin" />
                      {t.evaluatingBtn}
                    </>
                  ) : (
                    <>
                      {t.submitBtn}
                      <Send size={14} />
                    </>
                  )}
                </button>
              </div>
            </div>
          </div>

          {/* Note */}
          <p className="text-center text-[10px] text-slate-700 italic">
            *Note: This showcases the full functional Arena Layout with real-time agent presence.*
          </p>
        </div>
      </div>
    </div>
  )
}