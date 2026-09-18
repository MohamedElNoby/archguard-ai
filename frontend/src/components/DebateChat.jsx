import { useEffect, useRef } from 'react'
import { Shield, Activity, Wallet } from 'lucide-react'

// ── Agent config (visual only — labels come from t prop) ──────────────────

const AGENTS = {
  CyberSec: {
    key: 'CyberSec',
    icon: Shield,
    bg: 'bg-red-950/40',
    border: 'border-red-800/50',
    badge: 'bg-red-900/60 text-red-300',
    icon_color: 'text-red-400',
    ring: 'ring-red-800/40',
  },
  SRE: {
    key: 'SRE',
    icon: Activity,
    bg: 'bg-blue-950/40',
    border: 'border-blue-800/50',
    badge: 'bg-blue-900/60 text-blue-300',
    icon_color: 'text-blue-400',
    ring: 'ring-blue-800/40',
  },
  FinOps: {
    key: 'FinOps',
    icon: Wallet,
    bg: 'bg-emerald-950/40',
    border: 'border-emerald-800/50',
    badge: 'bg-emerald-900/60 text-emerald-300',
    icon_color: 'text-emerald-400',
    ring: 'ring-emerald-800/40',
  },
}

// ── Sub-components ────────────────────────────────────────────────────────

function TypingIndicator({ agent }) {
  const cfg = AGENTS[agent] ?? AGENTS.SRE
  const Icon = cfg.icon
  return (
    <div className={`msg-enter flex items-start gap-3 rounded-xl border p-4 ${cfg.bg} ${cfg.border}`}>
      <div className={`mt-0.5 shrink-0 rounded-lg p-1.5 ${cfg.badge} ring-1 ${cfg.ring}`}>
        <Icon size={14} className={cfg.icon_color} />
      </div>
      <div className="flex flex-col gap-1">
        <span className={`text-xs font-semibold ${cfg.icon_color}`}>{cfg.key}</span>
        <div className="flex items-center gap-1 py-1">
          <span className="typing-dot h-2 w-2 rounded-full bg-slate-400" />
          <span className="typing-dot h-2 w-2 rounded-full bg-slate-400" />
          <span className="typing-dot h-2 w-2 rounded-full bg-slate-400" />
        </div>
      </div>
    </div>
  )
}

function MessageCard({ message }) {
  const cfg = AGENTS[message.agent] ?? AGENTS.SRE
  const Icon = cfg.icon

  const time = message.timestamp
    ? new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    : null

  return (
    <div className={`msg-enter flex items-start gap-3 rounded-xl border p-4 ${cfg.bg} ${cfg.border}`}>
      <div className={`mt-0.5 shrink-0 rounded-lg p-1.5 ${cfg.badge} ring-1 ${cfg.ring}`}>
        <Icon size={14} className={cfg.icon_color} />
      </div>
      <div className="flex min-w-0 flex-1 flex-col gap-1">
        <div className="flex items-center justify-between gap-2">
          <span className={`text-xs font-semibold ${cfg.icon_color}`}>{cfg.key}</span>
          {time && <span className="text-[10px] text-slate-600">{time}</span>}
        </div>
        <p className="text-sm leading-relaxed text-slate-300 break-words">{message.message}</p>
      </div>
    </div>
  )
}

// ── Main component ────────────────────────────────────────────────────────

/**
 * DebateChat
 * Props:
 *   messages    {Array<{ agent, message, timestamp? }>}
 *   isTyping    {boolean}
 *   typingAgent {string}
 *   t           {object}  — translations.debate
 */
export default function DebateChat({ messages = [], isTyping = false, typingAgent = 'SRE', t }) {
  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isTyping])

  return (
    <div className="flex flex-col gap-2 rounded-2xl border border-slate-700/50 bg-slate-900/40 p-1">
      {/* Legend */}
      <div className="flex flex-wrap items-center gap-3 border-b border-slate-700/50 px-4 py-3">
        <span className="text-xs font-medium text-slate-500 me-1">{t.agentsLabel}</span>
        {Object.values(AGENTS).map((a) => {
          const Icon = a.icon
          return (
            <span
              key={a.key}
              className={`flex items-center gap-1.5 rounded-full px-2 py-0.5 text-xs font-medium ${a.badge}`}
            >
              <Icon size={11} /> {a.key}
            </span>
          )
        })}
      </div>

      {/* Messages */}
      <div className="flex max-h-[480px] flex-col gap-2 overflow-y-auto px-3 py-2 md:max-h-[560px]">
        {messages.length === 0 && !isTyping ? (
          <div className="flex flex-col items-center justify-center py-14 text-center text-slate-600">
            <Activity size={32} className="mb-3 opacity-40" />
            <p className="text-sm">{t.emptyTitle}</p>
            <p className="text-xs mt-1 opacity-70">{t.emptySubtitle}</p>
          </div>
        ) : (
          <>
            {messages.map((msg, i) => (
              <MessageCard key={i} message={msg} />
            ))}
            {isTyping && <TypingIndicator agent={typingAgent} />}
          </>
        )}
        <div ref={bottomRef} />
      </div>
    </div>
  )
}
