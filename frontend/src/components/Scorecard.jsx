import { CheckCircle2, TrendingUp, Award } from 'lucide-react'

// ── Score Ring ────────────────────────────────────────────────────────────

function ScoreRing({ score, max = 10 }) {
  const radius        = 44
  const circumference = 2 * Math.PI * radius
  const pct           = Math.min(Math.max(score / max, 0), 1)
  const offset        = circumference * (1 - pct)

  const color =
    pct >= 0.8 ? '#22c55e' :
    pct >= 0.6 ? '#f59e0b' :
                 '#ef4444'

  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="112" height="112" viewBox="0 0 112 112" className="-rotate-90">
        <circle cx="56" cy="56" r={radius} fill="none" stroke="#1e293b" strokeWidth="10" />
        <circle
          cx="56" cy="56" r={radius}
          fill="none"
          stroke={color}
          strokeWidth="10"
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          className="score-ring"
        />
      </svg>
      <div className="-mt-24 flex flex-col items-center">
        <span className="text-3xl font-extrabold text-slate-100">{score.toFixed(1)}</span>
        <span className="text-xs text-slate-500">/ {max}</span>
      </div>
      <div className="mt-14" />
    </div>
  )
}

// ── Progress bar ──────────────────────────────────────────────────────────

function CriterionBar({ name, value, max = 10, labelOverride }) {
  const pct = Math.min(Math.max((value / max) * 100, 0), 100)
  const bar =
    pct >= 80 ? 'bg-emerald-500' :
    pct >= 60 ? 'bg-amber-500'   :
                'bg-red-500'

  // Use translated label if provided, otherwise humanise snake_case
  const label = labelOverride
    ?? name.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase())

  return (
    <div className="flex flex-col gap-1.5">
      <div className="flex items-center justify-between text-xs">
        <span className="text-slate-400">{label}</span>
        <span className="font-semibold text-slate-300">{value.toFixed(1)}</span>
      </div>
      <div className="h-2 w-full overflow-hidden rounded-full bg-slate-800">
        <div
          className={`h-full rounded-full ${bar} transition-all duration-700`}
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  )
}

// ── Main Component ────────────────────────────────────────────────────────

/**
 * Scorecard
 * Props:
 *   evaluation {
 *     overall_score: number,
 *     criteria: { [key: string]: number },
 *     strengths: string[],
 *     improvement_recommendations: string[],
 *   }
 *   t {object} — translations.scorecard
 */
export default function Scorecard({ evaluation, t }) {
  if (!evaluation) return null

  const {
    overall_score               = 0,
    criteria                    = {},
    strengths                   = [],
    improvement_recommendations = [],
  } = evaluation

  const criteriaEntries = Object.entries(criteria)

  return (
    <div className="flex flex-col gap-5">
      {/* Overall Score */}
      <div className="rounded-2xl border border-slate-700/50 bg-slate-900/60 p-5">
        <div className="mb-4 flex items-center gap-2">
          <Award size={18} className="text-amber-400" />
          <h3 className="font-semibold text-slate-200">{t.overallScore}</h3>
        </div>
        <div className="flex items-center justify-center py-2">
          <ScoreRing score={overall_score} />
        </div>
      </div>

      {/* Criteria */}
      {criteriaEntries.length > 0 && (
        <div className="rounded-2xl border border-slate-700/50 bg-slate-900/60 p-5">
          <h3 className="mb-4 font-semibold text-slate-200">{t.criteria}</h3>
          <div className="flex flex-col gap-3">
            {criteriaEntries.map(([key, val]) => (
              <CriterionBar
                key={key}
                name={key}
                value={val}
                labelOverride={t.criteriaLabels?.[key]}
              />
            ))}
          </div>
        </div>
      )}

      {/* Strengths */}
      {strengths.length > 0 && (
        <div className="rounded-2xl border border-emerald-800/30 bg-emerald-950/20 p-5">
          <div className="mb-3 flex items-center gap-2">
            <CheckCircle2 size={16} className="text-emerald-400" />
            <h3 className="font-semibold text-slate-200">{t.strengths}</h3>
          </div>
          <ul className="flex flex-col gap-2">
            {strengths.map((s, i) => (
              <li key={i} className="flex items-start gap-2 text-sm text-slate-300">
                <span className="mt-1 shrink-0 h-1.5 w-1.5 rounded-full bg-emerald-500" />
                {s}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Improvement Recommendations */}
      {improvement_recommendations.length > 0 && (
        <div className="rounded-2xl border border-indigo-800/30 bg-indigo-950/20 p-5">
          <div className="mb-3 flex items-center gap-2">
            <TrendingUp size={16} className="text-indigo-400" />
            <h3 className="font-semibold text-slate-200">{t.recommendations}</h3>
          </div>
          <ul className="flex flex-col gap-2">
            {improvement_recommendations.map((r, i) => (
              <li key={i} className="flex items-start gap-2 text-sm text-slate-300">
                <span className="mt-1 shrink-0 h-1.5 w-1.5 rounded-full bg-indigo-400" />
                {r}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}
