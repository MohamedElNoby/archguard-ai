import { useState, useRef, useCallback } from 'react'
import { Upload, ImageIcon, FileCheck2, X, Zap, ChevronRight } from 'lucide-react'

/**
 * UploadPage
 * Props:
 *   onUpload  {(file: File | null) => void}  — called when user confirms (null = demo)
 *   t         {object}  — translations.upload
 *   isRTL     {boolean}
 */
export default function UploadPage({ onUpload, t, isRTL }) {
  const [file,      setFile]      = useState(null)
  const [preview,   setPreview]   = useState(null)   // data-URL for images
  const [dragging,  setDragging]  = useState(false)
  const inputRef = useRef(null)

  // ── file helpers ──────────────────────────────────────────────────────

  const acceptFile = useCallback((f) => {
    if (!f) return
    setFile(f)
    if (f.type.startsWith('image/')) {
      const reader = new FileReader()
      reader.onload = (e) => setPreview(e.target.result)
      reader.readAsDataURL(f)
    } else {
      setPreview(null)
    }
  }, [])

  const clearFile = () => { setFile(null); setPreview(null) }

  // ── drag events ───────────────────────────────────────────────────────

  const onDragOver  = (e) => { e.preventDefault(); setDragging(true)  }
  const onDragLeave = (e) => { e.preventDefault(); setDragging(false) }
  const onDrop      = (e) => {
    e.preventDefault()
    setDragging(false)
    const dropped = e.dataTransfer.files?.[0]
    if (dropped) acceptFile(dropped)
  }

  const onInputChange = (e) => {
    const picked = e.target.files?.[0]
    if (picked) acceptFile(picked)
    e.target.value = ''           // allow re-selecting same file
  }

  // ── render ─────────────────────────────────────────────────────────────

  return (
    <div className="flex flex-col items-center gap-8 py-4">
      {/* Page heading */}
      <div className="text-center">
        <h1 className="text-2xl font-extrabold tracking-tight text-slate-100 sm:text-3xl">
          {t.title}
        </h1>
        <p className="mt-2 max-w-xl text-sm text-slate-500">{t.subtitle}</p>
      </div>

      {/* Drop zone */}
      <div className="w-full max-w-2xl">
        {!file ? (
          <div
            onDragOver={onDragOver}
            onDragLeave={onDragLeave}
            onDrop={onDrop}
            onClick={() => inputRef.current?.click()}
            className={[
              'group relative flex cursor-pointer flex-col items-center justify-center gap-4 rounded-2xl border-2 border-dashed px-8 py-16 text-center transition-all duration-200',
              dragging
                ? 'border-indigo-500 bg-indigo-950/30 scale-[1.01]'
                : 'border-slate-700 bg-slate-900/40 hover:border-indigo-600/60 hover:bg-slate-900/60',
            ].join(' ')}
          >
            {/* Icon */}
            <div className={[
              'flex h-16 w-16 items-center justify-center rounded-2xl transition-colors duration-200',
              dragging ? 'bg-indigo-600/30' : 'bg-slate-800 group-hover:bg-indigo-900/30',
            ].join(' ')}>
              <Upload size={28} className={dragging ? 'text-indigo-400' : 'text-slate-500 group-hover:text-indigo-400'} />
            </div>

            <div>
              <p className="text-base font-semibold text-slate-300">{t.dragText}</p>
              <p className="mt-1 text-sm text-slate-600">{t.orText}</p>
            </div>

            <button
              type="button"
              onClick={(e) => { e.stopPropagation(); inputRef.current?.click() }}
              className="rounded-xl border border-indigo-600/50 bg-indigo-600/10 px-5 py-2 text-sm font-semibold text-indigo-300 transition hover:bg-indigo-600/20"
            >
              {t.browseBtn}
            </button>

            <p className="text-xs text-slate-700">{t.formats}</p>

            <input
              ref={inputRef}
              type="file"
              accept="image/png,image/jpeg,image/svg+xml,application/pdf"
              className="hidden"
              onChange={onInputChange}
            />
          </div>
        ) : (
          /* ── Preview card after file selected ── */
          <div className="relative rounded-2xl border border-slate-700/60 bg-slate-900/60 p-4">
            {/* Clear button */}
            <button
              onClick={clearFile}
              className="absolute end-3 top-3 rounded-full bg-slate-800 p-1.5 text-slate-400 transition hover:bg-slate-700 hover:text-white"
              aria-label="Remove file"
            >
              <X size={14} />
            </button>

            {preview ? (
              /* Image preview */
              <div className="overflow-hidden rounded-xl border border-slate-700/40">
                <img
                  src={preview}
                  alt="Architecture preview"
                  className="max-h-72 w-full object-contain bg-slate-950"
                />
              </div>
            ) : (
              /* Non-image file */
              <div className="flex items-center gap-3 rounded-xl border border-slate-700/40 bg-slate-800/60 px-4 py-5">
                <FileCheck2 size={28} className="shrink-0 text-indigo-400" />
                <div className="min-w-0">
                  <p className="truncate text-sm font-semibold text-slate-200">{file.name}</p>
                  <p className="text-xs text-slate-500">{(file.size / 1024).toFixed(1)} KB</p>
                </div>
              </div>
            )}

            {/* File name row */}
            <div className="mt-3 flex items-center gap-2 text-xs text-slate-500">
              <ImageIcon size={12} />
              <span className="truncate">{t.fileName} <span className="text-slate-400">{file.name}</span></span>
            </div>

            {/* Change file */}
            <button
              onClick={() => { clearFile(); setTimeout(() => inputRef.current?.click(), 50) }}
              className="mt-2 text-xs text-indigo-400 underline-offset-2 hover:underline"
            >
              {t.changeBtn}
            </button>

            <input
              ref={inputRef}
              type="file"
              accept="image/png,image/jpeg,image/svg+xml,application/pdf"
              className="hidden"
              onChange={onInputChange}
            />
          </div>
        )}
      </div>

      {/* Action buttons */}
      <div className="flex flex-col items-center gap-3 w-full max-w-2xl">
        {/* Primary — analyse (enabled only when file chosen) */}
        <button
          onClick={() => onUpload(file)}
          disabled={!file}
          className="flex w-full items-center justify-center gap-2 rounded-xl bg-indigo-600 px-8 py-3 text-sm font-semibold text-white shadow-xl shadow-indigo-900/30 transition hover:bg-indigo-500 active:scale-95 disabled:cursor-not-allowed disabled:opacity-40"
        >
          {t.analyzeBtn}
          <ChevronRight size={16} className={isRTL ? 'rtl-flip' : ''} />
        </button>

        {/* Divider */}
        <div className="flex w-full items-center gap-3 text-xs text-slate-700">
          <div className="h-px flex-1 bg-slate-800" />
          <span>{t.orText}</span>
          <div className="h-px flex-1 bg-slate-800" />
        </div>

        {/* Demo shortcut */}
        <div className="flex flex-col items-center gap-1.5">
          <button
            onClick={() => onUpload(null)}
            className="flex items-center gap-2 rounded-xl border border-slate-700/50 bg-slate-800/60 px-6 py-2.5 text-sm font-semibold text-slate-300 transition hover:border-indigo-600/40 hover:text-indigo-300 active:scale-95"
          >
            <Zap size={15} className="text-amber-400" />
            {t.demoBtn}
          </button>
          <p className="text-center text-xs text-slate-600 max-w-sm">{t.demoHint}</p>
        </div>
      </div>
    </div>
  )
}
