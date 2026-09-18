import { useEffect, useRef, useState } from 'react'
import mermaid from 'mermaid'

// Initialise once with a dark theme
mermaid.initialize({
  startOnLoad: false,
  theme: 'dark',
  themeVariables: {
    background: '#0f1629',
    primaryColor: '#1e3a5f',
    primaryTextColor: '#e2e8f0',
    lineColor: '#475569',
    fontSize: '14px',
  },
  securityLevel: 'loose',
})

let idCounter = 0

/**
 * MermaidViewer
 * Props:
 *   mermaid_diagram {string}  — Mermaid diagram source
 */
export default function MermaidViewer({ mermaid_diagram }) {
  const containerRef = useRef(null)
  const [error, setError]     = useState(null)
  const [svg, setSvg]         = useState('')
  const diagramId = useRef(`mermaid-${++idCounter}`)

  useEffect(() => {
    if (!mermaid_diagram?.trim()) {
      setSvg('')
      setError(null)
      return
    }

    setError(null)

    const render = async () => {
      try {
        const { svg: rendered } = await mermaid.render(
          diagramId.current,
          mermaid_diagram.trim(),
        )
        setSvg(rendered)
        // bump id so next render call uses a fresh element
        diagramId.current = `mermaid-${++idCounter}`
      } catch (err) {
        console.warn('Mermaid render error:', err)
        setError('Invalid diagram syntax. Please check the Mermaid code.')
        setSvg('')
      }
    }

    render()
  }, [mermaid_diagram])

  if (!mermaid_diagram?.trim()) return null

  return (
    <div className="w-full">
      {error ? (
        <div className="rounded-lg border border-red-800/50 bg-red-950/30 px-4 py-3 text-sm text-red-400">
          ⚠ {error}
        </div>
      ) : svg ? (
        <div
          className="mermaid-scroll rounded-xl border border-slate-700/50 bg-slate-900/60 p-4"
          ref={containerRef}
          dangerouslySetInnerHTML={{ __html: svg }}
        />
      ) : (
        <div className="flex items-center justify-center rounded-xl border border-slate-700/50 bg-slate-900/60 py-10 text-sm text-slate-500">
          <span className="mr-2 animate-spin">⟳</span> Rendering diagram…
        </div>
      )}
    </div>
  )
}
