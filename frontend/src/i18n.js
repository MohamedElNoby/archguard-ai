/**
 * i18n.js — All user-facing strings for English and Arabic.
 *
 * Usage:
 *   import { translations } from './i18n.js'
 *   const t = translations[lang]   // lang = 'en' | 'ar'
 *   t.header.title                 // → "ArchGuard AI"  /  "آرك‌غارد AI"
 */

export const translations = {
  en: {
    // ── Header ──────────────────────────────────────────────────────────
    header: {
      brand:   'ArchGuard',
      restart: 'Restart',
    },

    // ── Stepper ──────────────────────────────────────────────────────────
    stepper: {
      steps: ['Upload Architecture', 'Risk & Debate', 'Arena Defense', 'Evaluation'],
    },

    // ── Stage 0 — Upload ─────────────────────────────────────────────────
    upload: {
      title:        'Upload Your Architecture',
      subtitle:     'Upload a diagram or image of your system architecture. The AI jury will analyse it and identify risks.',
      dragText:     'Drag & drop your architecture image here',
      orText:       'or',
      browseBtn:    'Browse File',
      formats:      'Supports PNG, JPG, SVG, PDF — max 10 MB',
      uploading:    'Uploading…',
      analyzeBtn:   'Analyse Architecture',
      changeBtn:    'Change File',
      fileName:     'Selected file:',
      demoBtn:      'Use Demo Architecture',
      demoHint:     'No image? Use a built-in demo scenario to explore the full flow.',
    },

    // ── Stage 1 ──────────────────────────────────────────────────────────
    stage1: {
      title:       'Architectural Risk Analysis',
      subtitle:    'Watch three AI agents debate the primary architectural risk before you craft your defense.',
      startBtn:    'Start Live Debate',
      loadingBtn:  'Loading Scenario…',
      liveDebate:  'Live Debate',
      proceedBtn:  'Proceed to Defense',
    },

    // ── Stage 2 — Arena Defense ──────────────────────────────────────────
    stage2: {
      title:            'Architectural Jury: Live Session',
      subtitle:         'Watch the jury debate, then submit your defense plan.',
      recapTitle:       'Architecture Recap',
      recapDesc:        'Summarized diagram view of the system uploaded.',
      discoveredRisks:  'Discovered Risks:',
      juryDebateTitle:  'Jury Debate',
      challengeLabel:   '🚧 ADVERSARIAL CHALLENGE — Submit Your Plan 🚧',
      placeholder:      'Type your defense plan here…',
      charsRemaining:   'characters remaining',
      submitBtn:        'Submit Defense',
      evaluatingBtn:    'Evaluating…',
      agentStatus: {
        CyberSec: { role: 'CyberSec 🔴', status: '🛡 Listening', focus: 'Focus: Threats & Exploits.' },
        SRE:      { role: 'SRE 🔵',      status: '⚡ Challenging', focus: 'Focus: Scalability & Reliability.' },
        FinOps:   { role: 'FinOps 🟢',   status: '💰 Analyzing',  focus: 'Focus: Cost & Efficiency.' },
      },
      riskLabel:        'Risk to address:',
    },

    // ── Stage 3 ──────────────────────────────────────────────────────────
    stage3: {
      title:              'Evaluation Result',
      subtitle:           'Here is the AI evaluation of your architectural defense.',
      correctedArch:      'Corrected Architecture',
      noDiagram:          'No corrected diagram provided.',
      newSession:         'Start New Session',
    },

    // ── PrimaryRiskCard ──────────────────────────────────────────────────
    riskCard: {
      label: 'Primary Risk',
      levels: {
        Critical: 'Critical',
        High:     'High',
        Medium:   'Medium',
        Low:      'Low',
      },
    },

    // ── DebateChat ───────────────────────────────────────────────────────
    debate: {
      agentsLabel:      'Agents:',
      emptyTitle:       "The debate hasn't started yet.",
      emptySubtitle:    'Trigger a debate to watch the agents discuss.',
    },

    // ── DefenseInput ─────────────────────────────────────────────────────
    defense: {
      title:        'Your Architectural Defense',
      hint:         'Explain how you would redesign the architecture to address the primary risk identified above. Be specific about patterns, tools, and trade-offs.',
      placeholder:  'Describe your architectural solution here…',
      ctrlEnterTip: 'Tip: Press Ctrl+Enter to submit.',
      fillDemo:     'Fill Demo Defense',
      submit:       'Submit Defense',
      evaluating:   'Evaluating Defense…',
    },

    // ── Scorecard ────────────────────────────────────────────────────────
    scorecard: {
      overallScore:      'Overall Score',
      criteria:          'Evaluation Criteria',
      strengths:         'Strengths',
      recommendations:   'Improvement Recommendations',
      criteriaLabels: {
        risk_understanding:   'Risk Understanding',
        technical_reasoning:  'Technical Reasoning',
        architecture_quality: 'Architecture Quality',
        scalability:          'Scalability',
        cost_awareness:       'Cost Awareness',
      },
    },

    // ── Error / misc ──────────────────────────────────────────────────────
    misc: {
      error:            'Something went wrong. Please try again.',
      renderingDiagram: 'Rendering diagram…',
      invalidDiagram:   'Invalid diagram syntax. Please check the Mermaid code.',
    },

    // ── Footer ────────────────────────────────────────────────────────────
    footer: 'ArchGuard AI — Architecture Evaluation Platform',
  },

  // ════════════════════════════════════════════════════════════════════════
  ar: {
    // ── Header ──────────────────────────────────────────────────────────
    header: {
      brand:   'آرك‌غارد',
      restart: 'إعادة البدء',
    },

    // ── Stepper ──────────────────────────────────────────────────────────
    stepper: {
      steps: ['رفع المعمارية', 'المخاطر والنقاش', 'ساحة الدفاع', 'التقييم'],
    },

    // ── Stage 0 — Upload ─────────────────────────────────────────────────
    upload: {
      title:        'ارفع مخطط المعمارية',
      subtitle:     'ارفع مخططاً أو صورة لمعمارية نظامك. سيقوم وكلاء الذكاء الاصطناعي بتحليله وتحديد المخاطر.',
      dragText:     'اسحب وأفلت صورة المعمارية هنا',
      orText:       'أو',
      browseBtn:    'تصفح الملفات',
      formats:      'يدعم PNG، JPG، SVG، PDF — بحد أقصى 10 ميغابايت',
      uploading:    'جارٍ الرفع…',
      analyzeBtn:   'تحليل المعمارية',
      changeBtn:    'تغيير الملف',
      fileName:     'الملف المحدد:',
      demoBtn:      'استخدام معمارية تجريبية',
      demoHint:     'لا توجد صورة؟ استخدم سيناريو تجريبياً مدمجاً لاستكشاف التدفق الكامل.',
    },

    // ── Stage 1 ──────────────────────────────────────────────────────────
    stage1: {
      title:       'تحليل مخاطر المعمارية',
      subtitle:    'شاهد ثلاثة وكلاء ذكاء اصطناعي يناقشون المخاطر المعمارية الرئيسية قبل أن تُعدّ دفاعك.',
      startBtn:    'بدء النقاش المباشر',
      loadingBtn:  'جارٍ تحميل السيناريو…',
      liveDebate:  'نقاش مباشر',
      proceedBtn:  'الانتقال إلى الدفاع',
    },

    // ── Stage 2 — Arena Defense ──────────────────────────────────────────
    stage2: {
      title:            'هيئة المحلفين المعمارية: جلسة مباشرة',
      subtitle:         'شاهد نقاش هيئة المحلفين، ثم قدّم خطة دفاعك.',
      recapTitle:       'ملخص المعمارية',
      recapDesc:        'عرض مبسّط للمخطط الذي تم رفعه.',
      discoveredRisks:  'المخاطر المكتشفة:',
      juryDebateTitle:  'نقاش هيئة المحلفين',
      challengeLabel:   '🚧 التحدي العدائي — قدّم خطتك 🚧',
      placeholder:      'اكتب خطة دفاعك هنا…',
      charsRemaining:   'حرف متبقٍّ',
      submitBtn:        'إرسال الدفاع',
      evaluatingBtn:    'جارٍ التقييم…',
      agentStatus: {
        CyberSec: { role: 'CyberSec 🔴', status: '🛡 مستمع',  focus: 'التركيز: التهديدات والثغرات.' },
        SRE:      { role: 'SRE 🔵',      status: '⚡ متحدٍّ', focus: 'التركيز: التوسع والموثوقية.' },
        FinOps:   { role: 'FinOps 🟢',   status: '💰 محلّل',  focus: 'التركيز: التكلفة والكفاءة.' },
      },
      riskLabel:        'الخطر المطلوب معالجته:',
    },

    // ── Stage 3 ──────────────────────────────────────────────────────────
    stage3: {
      title:              'نتيجة التقييم',
      subtitle:           'هذا هو تقييم الذكاء الاصطناعي لدفاعك المعماري.',
      correctedArch:      'المعمارية المُصحَّحة',
      noDiagram:          'لم يُقدَّم مخطط مُصحَّح.',
      newSession:         'بدء جلسة جديدة',
    },

    // ── PrimaryRiskCard ──────────────────────────────────────────────────
    riskCard: {
      label: 'المخاطر الرئيسية',
      levels: {
        Critical: 'حرج',
        High:     'عالٍ',
        Medium:   'متوسط',
        Low:      'منخفض',
      },
    },

    // ── DebateChat ───────────────────────────────────────────────────────
    debate: {
      agentsLabel:      'الوكلاء:',
      emptyTitle:       'لم يبدأ النقاش بعد.',
      emptySubtitle:    'ابدأ نقاشاً لمشاهدة الوكلاء يتحدثون.',
    },

    // ── DefenseInput ─────────────────────────────────────────────────────
    defense: {
      title:        'دفاعك المعماري',
      hint:         'اشرح كيف ستُعيد تصميم المعمارية لمعالجة الخطر الرئيسي المحدّد. كن دقيقاً في الأنماط والأدوات والمقايضات.',
      placeholder:  'صِف حلّك المعماري هنا…',
      ctrlEnterTip: 'نصيحة: اضغط Ctrl+Enter للإرسال.',
      fillDemo:     'ملء دفاع تجريبي',
      submit:       'إرسال الدفاع',
      evaluating:   'جارٍ تقييم الدفاع…',
    },

    // ── Scorecard ────────────────────────────────────────────────────────
    scorecard: {
      overallScore:      'الدرجة الإجمالية',
      criteria:          'معايير التقييم',
      strengths:         'نقاط القوة',
      recommendations:   'توصيات التحسين',
      criteriaLabels: {
        risk_understanding:   'فهم المخاطر',
        technical_reasoning:  'التفكير التقني',
        architecture_quality: 'جودة المعمارية',
        scalability:          'قابلية التوسع',
        cost_awareness:       'الوعي بالتكاليف',
      },
    },

    // ── Error / misc ──────────────────────────────────────────────────────
    misc: {
      error:            'حدث خطأ ما. يرجى المحاولة مرة أخرى.',
      renderingDiagram: 'جارٍ تصيير المخطط…',
      invalidDiagram:   'صيغة المخطط غير صالحة. يرجى مراجعة كود Mermaid.',
    },

    // ── Footer ────────────────────────────────────────────────────────────
    footer: 'آرك‌غارد AI — منصة تقييم المعمارية',
  },
}

/** Arabic demo defense text shown when "Fill Demo Defense" is clicked in AR mode */
export const DEMO_DEFENSE_AR = `لمعالجة خطر الفشل المتتالي الناجم عن التسلسل المتزامن، أقترح التغييرات المعمارية التالية:

١. نمط قاطع الدائرة (Circuit Breaker): تطبيق قواطع دائرة بين جميع حدود الخدمات المتزامنة باستخدام Resilience4j أو شبكة خدمات مثل Istio. عند تجاوز حدّ الفشل، يُفتح القاطع ويرفض الطلبات فوراً بدلاً من إبقاء الخيوط البرمجية معلّقة.

٢. فصل غير متزامن (Async Decoupling): استبدال الاستدعاءات المتزامنة في المسارات غير الحرجة بنهج قائم على الأحداث باستخدام وسيط رسائل مثل Apache Kafka أو AWS SQS. يعزل هذا نطاقات الفشل حتى لا يتصاعد تدهور خدمة واحدة إلى الأعلى.

٣. عزل الحاجز (Bulkhead Isolation): تطبيق أنماط الحاجز باستخدام عزل مجموعة الخيوط لكل اعتماد خارجي، مما يمنع استنزاف مجموعة الخيوط المشتركة.

٤. المهلة وإعادة المحاولة مع التراجع التدريجي: فرض مهلات صارمة لكل خطوة (مثلاً 500 ملي ثانية) واستخدام التراجع الأسي مع الاضطراب لتقليل آثار قطعان الرعد أثناء الاسترداد.

٥. قابلية الملاحظة: إضافة تتبع موزع (OpenTelemetry) وتنبيهات ميزانية الخطأ حتى يتمكن فريق SRE من اكتشاف الأعطال الجزئية قبل تفاقمها.

من منظور التكلفة، يعد المسار المبني على الأحداث باستخدام الخدمات المُدارة (SQS, SNS) أكثر فعالية من حيث التكلفة مقارنةً بزيادة الموارد الحسابية لاستيعاب عواصف إعادة المحاولة المتزامنة.`
