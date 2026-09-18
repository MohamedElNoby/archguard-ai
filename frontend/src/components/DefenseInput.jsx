import { useState } from 'react'
import { Send, Loader2, FileText } from 'lucide-react'
import { DEMO_DEFENSE_AR } from '../i18n.js'

const DEMO_DEFENSE_EN = `To address the cascading failure risk introduced by synchronous service chaining, I propose the following architectural changes:

1. Circuit Breaker Pattern: Introduce circuit breakers (e.g., using Resilience4j or a service mesh like Istio) between all synchronous service boundaries. When a downstream service exceeds the failure threshold, the circuit opens and fast-fails requests instead of holding threads.

2. Asynchronous Decoupling: Replace synchronous calls for non-critical paths with an event-driven approach using a message broker such as Apache Kafka or AWS SQS. This isolates failure domains so that one service degradation does not propagate upstream.

3. Bulkhead Isolation: Apply bulkhead patterns using thread-pool isolation per downstream dependency. This prevents a slow external call from exhausting the shared thread pool.

4. Timeouts and Retries with Backoff: Enforce strict per-hop timeouts (e.g., 500ms) and use exponential backoff with jitter for retries to reduce thundering-herd effects during recovery.

5. Observability: Add distributed tracing (OpenTelemetry) and error-budget alerting so the SRE team can detect partial failures before they escalate.

From a cost perspective, the event-driven path using managed services (SQS, SNS) is more cost-effective than over-provisioning compute to absorb synchronous retry storms. The circuit breaker approach also reduces wasted CPU and cloud billing during incidents.`

/**
 * DefenseInput
 * Props:
 *   onSubmit {(defenseText: string) => void}
 *   loading  {boolean}
 *   t        {object}  — translations.defense
 *   lang     {string}  — 'en' | 'ar'
 */
export default function DefenseInput({ onSubmit, loading = false, t, lang = 'en' }) {
  const [text, setText] = useState('')

  const handleSubmit = () => {
    const trimmed = text.trim()
    if (!trimmed || loading) return
    onSubmit(trimmed)
  }

  const handleKeyDown = (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
      e.preventDefault()
      handleSubmit()
    }
  }

  const fillDemo = () => setText(lang === 'ar' ? DEMO_DEFENSE_AR : DEMO_DEFENSE_EN)
  const isEmpty  = !text.trim()

  return (
    <div className="rounded-2xl border border-slate-700/50 bg-slate-900/40 p-5">
      {/* Title */}
      <div className="mb-4 flex items-center gap-2">
        <FileText size={18} className="text-indigo-400" />
        <h3 className="font-semibold text-slate-200">{t.title}</h3>
      </div>

      <p className="mb-3 text-xs text-slate-500">{t.hint}</p>

      {/* Textarea — dir forced to match UI, but user can type either direction */}
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        onKeyDown={handleKeyDown}
        disabled={loading}
        placeholder={t.placeholder}
        rows={8}
        className="w-full resize-y rounded-xl border border-slate-700/60 bg-slate-800/60 px-4 py-3 text-sm text-slate-200 placeholder-slate-600 outline-none transition focus:border-indigo-600/70 focus:ring-1 focus:ring-indigo-600/40 disabled:cursor-not-allowed disabled:opacity-50"
      />

      <p className="mt-1.5 text-[10px] text-slate-600">{t.ctrlEnterTip}</p>

      {/* Actions */}
      <div className="mt-4 flex flex-wrap items-center justify-between gap-3">
        <button
          onClick={fillDemo}
          disabled={loading}
          className="flex items-center gap-1.5 rounded-lg border border-slate-700/50 bg-slate-800/60 px-3 py-2 text-xs text-slate-400 transition hover:border-slate-600 hover:text-slate-200 disabled:cursor-not-allowed disabled:opacity-40"
        >
          <FileText size={13} />
          {t.fillDemo}
        </button>

        <button
          onClick={handleSubmit}
          disabled={loading || isEmpty}
          className="flex items-center gap-2 rounded-xl bg-indigo-600 px-5 py-2.5 text-sm font-semibold text-white shadow-lg shadow-indigo-900/30 transition hover:bg-indigo-500 active:scale-95 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {loading ? (
            <>
              <Loader2 size={15} className="animate-spin" />
              {t.evaluating}
            </>
          ) : (
            <>
              <Send size={15} />
              {t.submit}
            </>
          )}
        </button>
      </div>
    </div>
  )
}
