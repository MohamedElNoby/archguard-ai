import { AlertTriangle, AlertOctagon, AlertCircle, Info } from 'lucide-react'

const LEVEL_CONFIG = {
  Critical: {
    border: 'border-red-700/60',
    bg: 'bg-red-950/40',
    badge: 'bg-red-900 text-red-300',
    icon: AlertOctagon,
    icon_color: 'text-red-400',
    glow: 'shadow-red-900/30',
  },
  High: {
    border: 'border-orange-700/60',
    bg: 'bg-orange-950/30',
    badge: 'bg-orange-900 text-orange-300',
    icon: AlertTriangle,
    icon_color: 'text-orange-400',
    glow: 'shadow-orange-900/30',
  },
  Medium: {
    border: 'border-yellow-700/60',
    bg: 'bg-yellow-950/20',
    badge: 'bg-yellow-900 text-yellow-300',
    icon: AlertCircle,
    icon_color: 'text-yellow-400',
    glow: 'shadow-yellow-900/20',
  },
  Low: {
    border: 'border-blue-700/60',
    bg: 'bg-blue-950/20',
    badge: 'bg-blue-900 text-blue-300',
    icon: Info,
    icon_color: 'text-blue-400',
    glow: 'shadow-blue-900/20',
  },
}

/**
 * PrimaryRiskCard
 * Props:
 *   risk {
 *     title: string,
 *     level: "Critical" | "High" | "Medium" | "Low",
 *     description: string,
 *   }
 *   t {object} — translations.riskCard
 */
export default function PrimaryRiskCard({ risk, t }) {
  if (!risk) return null

  const level = risk.level ?? 'High'
  const cfg   = LEVEL_CONFIG[level] ?? LEVEL_CONFIG.High
  const Icon  = cfg.icon

  // Translated level label (falls back to the English key if not found)
  const levelLabel = t?.levels?.[level] ?? level

  return (
    <div className={`rounded-2xl border ${cfg.border} ${cfg.bg} p-5 shadow-lg ${cfg.glow}`}>
      {/* Header */}
      <div className="mb-4 flex items-start justify-between gap-3">
        <div className="flex items-center gap-3">
          <div className={`rounded-xl p-2.5 ${cfg.badge}`}>
            <Icon size={20} className={cfg.icon_color} />
          </div>
          <div>
            <p className="text-[10px] font-semibold uppercase tracking-widest text-slate-500">
              {t?.label ?? 'Primary Risk'}
            </p>
            <h2 className="text-base font-bold leading-snug text-slate-100 sm:text-lg">
              {risk.title}
            </h2>
          </div>
        </div>
        <span className={`shrink-0 rounded-full px-3 py-1 text-xs font-bold uppercase tracking-wide ${cfg.badge}`}>
          {levelLabel}
        </span>
      </div>

      {/* Divider */}
      <div className={`mb-4 h-px w-full ${cfg.border} opacity-50`} />

      {/* Description */}
      <p className="text-sm leading-relaxed text-slate-400">
        {risk.description}
      </p>
    </div>
  )
}
