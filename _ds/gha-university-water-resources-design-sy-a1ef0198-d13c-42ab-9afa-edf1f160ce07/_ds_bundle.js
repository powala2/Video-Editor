/* @ds-bundle: {"format":4,"namespace":"GHAUniversityWaterResourcesDesignSystem_a1ef01","components":[{"name":"DisclosureCard","sourcePath":"components/data/DisclosureCard.jsx"},{"name":"MatrixCell","sourcePath":"components/data/MatrixCell.jsx"},{"name":"LessonToggleCell","sourcePath":"components/data/MatrixCell.jsx"},{"name":"ResourceRow","sourcePath":"components/data/ResourceRow.jsx"},{"name":"Surface","sourcePath":"components/data/Surface.jsx"},{"name":"Avatar","sourcePath":"components/feedback/Avatar.jsx"},{"name":"CountBadge","sourcePath":"components/feedback/CountBadge.jsx"},{"name":"LaborBadge","sourcePath":"components/feedback/LaborBadge.jsx"},{"name":"LevelBadge","sourcePath":"components/feedback/LevelBadge.jsx"},{"name":"ProficiencyChip","sourcePath":"components/feedback/ProficiencyChip.jsx"},{"name":"SKILL_PROFICIENCY","sourcePath":"components/feedback/ProficiencyChip.jsx"},{"name":"ProgressBar","sourcePath":"components/feedback/ProgressBar.jsx"},{"name":"StatusPill","sourcePath":"components/feedback/StatusPill.jsx"},{"name":"Button","sourcePath":"components/forms/Button.jsx"},{"name":"IconButton","sourcePath":"components/forms/IconButton.jsx"},{"name":"InlineEditText","sourcePath":"components/forms/InlineEditText.jsx"},{"name":"Input","sourcePath":"components/forms/Input.jsx"},{"name":"Select","sourcePath":"components/forms/Input.jsx"},{"name":"FormField","sourcePath":"components/forms/Input.jsx"},{"name":"SearchBar","sourcePath":"components/forms/SearchBar.jsx"},{"name":"NoResults","sourcePath":"components/forms/SearchBar.jsx"},{"name":"Icon","sourcePath":"components/icons/Icon.jsx"},{"name":"GripIcon","sourcePath":"components/icons/Icon.jsx"},{"name":"ICON_NAMES","sourcePath":"components/icons/Icon.jsx"},{"name":"Header","sourcePath":"components/layout/Header.jsx"},{"name":"Logo","sourcePath":"components/layout/Logo.jsx"},{"name":"PageContent","sourcePath":"components/layout/PageContent.jsx"},{"name":"Sidebar","sourcePath":"components/layout/Sidebar.jsx"},{"name":"Modal","sourcePath":"components/overlay/Modal.jsx"},{"name":"ModalHead","sourcePath":"components/overlay/Modal.jsx"},{"name":"ModalBody","sourcePath":"components/overlay/Modal.jsx"},{"name":"ModalFoot","sourcePath":"components/overlay/Modal.jsx"},{"name":"ConfirmModal","sourcePath":"components/overlay/Modal.jsx"},{"name":"CancelButton","sourcePath":"components/overlay/Modal.jsx"},{"name":"PrimarySaveButton","sourcePath":"components/overlay/Modal.jsx"},{"name":"DangerSaveButton","sourcePath":"components/overlay/Modal.jsx"}],"sourceHashes":{"components/data/DisclosureCard.jsx":"7277881ee86b","components/data/MatrixCell.jsx":"7eca30a82e75","components/data/ResourceRow.jsx":"60514b5f7d86","components/data/Surface.jsx":"6f0909253472","components/feedback/Avatar.jsx":"e4779075bae1","components/feedback/CountBadge.jsx":"3ddfaa76e3a3","components/feedback/LaborBadge.jsx":"2bc212c9fba4","components/feedback/LevelBadge.jsx":"3c53d420aecf","components/feedback/ProficiencyChip.jsx":"a8d3604e45c1","components/feedback/ProgressBar.jsx":"0ed3c44c570c","components/feedback/StatusPill.jsx":"ffe4cef87502","components/forms/Button.jsx":"7c4b3e9eed12","components/forms/IconButton.jsx":"1cef0004efa5","components/forms/InlineEditText.jsx":"f296973ce6d1","components/forms/Input.jsx":"7abb14016d7e","components/forms/SearchBar.jsx":"13cb8816ee70","components/icons/Icon.jsx":"a36d83184815","components/layout/Header.jsx":"2c83c004c67f","components/layout/Logo.jsx":"44a9a28ece91","components/layout/PageContent.jsx":"ca767aedfedd","components/layout/Sidebar.jsx":"9c7627704469","components/overlay/Modal.jsx":"8798b45841f8","ui_kits/water-resources-lms/App.jsx":"484abe301522","ui_kits/water-resources-lms/AssignmentsScreen.jsx":"756c623f5d37","ui_kits/water-resources-lms/CurriculumScreen.jsx":"515b50a8afd7","ui_kits/water-resources-lms/DatabaseScreen.jsx":"071222b13f33","ui_kits/water-resources-lms/LoginScreen.jsx":"74bb3baa8c83","ui_kits/water-resources-lms/MatrixScreen.jsx":"e8f5eeaed759","ui_kits/water-resources-lms/SkillsScreen.jsx":"050afcaeccbb","ui_kits/water-resources-lms/data.js":"f61439bd9045","ui_kits/water-resources-lms/helpers.js":"66a10792c680"},"inlinedExternals":[],"unexposedExports":[{"name":"resourceMeta","sourcePath":"components/data/ResourceRow.jsx"}]} */

(() => {

const __ds_ns = (window.GHAUniversityWaterResourcesDesignSystem_a1ef01 = window.GHAUniversityWaterResourcesDesignSystem_a1ef01 || {});

const __ds_scope = {};

(__ds_ns.__errors = __ds_ns.__errors || []);

// components/data/MatrixCell.jsx
try { (() => {
/**
 * MatrixCell — the small status button used in Matrix/Skills grid tables:
 * empty / in-progress (fraction) / done (✓), plus an interactive variant
 * for per-lesson toggles. Copied from MatrixView .cellBtn/.lessonCellBtn.
 */
function MatrixCell({
  state = 'empty',
  label = '',
  size = 30,
  onClick,
  title
}) {
  const styles = {
    empty: {
      background: '#F6F3EC',
      border: '1px solid #ECE6D8',
      color: '#B7B29A'
    },
    prog: {
      background: 'var(--warning-swatch)',
      border: 'none',
      color: '#7A5B12'
    },
    done: {
      background: 'var(--primary-hex)',
      border: 'none',
      color: '#fff'
    }
  };
  const s = styles[state] || styles.empty;
  return /*#__PURE__*/React.createElement("button", {
    onClick: onClick,
    title: title,
    style: {
      minWidth: size,
      height: size,
      padding: '0 6px',
      borderRadius: 8,
      cursor: onClick ? 'pointer' : 'default',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      font: `700 ${state === 'prog' ? 10 : 13}px var(--font-sans)`,
      ...s
    }
  }, state === 'done' ? '✓' : label);
}

/** Small 22px per-lesson toggle cell (Matrix expanded rows). */
function LessonToggleCell({
  done,
  available = true,
  onClick,
  title
}) {
  return /*#__PURE__*/React.createElement("button", {
    onClick: onClick,
    title: title,
    style: {
      width: 22,
      height: 22,
      borderRadius: 6,
      cursor: 'pointer',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      font: '700 12px var(--font-sans)',
      border: `1.5px solid ${done ? 'var(--primary-hex)' : available ? '#C6BFA9' : '#E4D0C4'}`,
      background: done ? 'var(--primary-hex)' : available ? '#fff' : '#FBF4F0',
      color: '#fff'
    }
  }, done ? '✓' : '');
}
Object.assign(__ds_scope, { MatrixCell, LessonToggleCell });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/data/MatrixCell.jsx", error: String((e && e.message) || e) }); }

// components/data/Surface.jsx
try { (() => {
/** Surface — plain elevated panel, no disclosure (Matrix/Skills table wrap, static panels). */
function Surface({
  children,
  style
}) {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      background: 'var(--surface)',
      border: '1px solid var(--border)',
      borderRadius: 16,
      boxShadow: 'var(--shadow-card)',
      overflow: 'hidden',
      ...style
    }
  }, children);
}
Object.assign(__ds_scope, { Surface });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/data/Surface.jsx", error: String((e && e.message) || e) }); }

// components/feedback/Avatar.jsx
try { (() => {
function initials(name) {
  return (name || '').trim().split(/\s+/).map(w => w[0] || '').slice(0, 2).join('').toUpperCase() || '?';
}

/** Avatar — initials circle, forest-green fill. Copied from Sidebar/AssignmentsView/MatrixView avatar treatment. */
function Avatar({
  name,
  size = 30
}) {
  return /*#__PURE__*/React.createElement("span", {
    style: {
      width: size,
      height: size,
      flex: 'none',
      borderRadius: '50%',
      background: 'var(--avatar-bg)',
      color: 'var(--avatar-ink)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      font: `800 ${Math.round(size * 0.37)}px var(--font-sans)`
    }
  }, initials(name));
}
Object.assign(__ds_scope, { Avatar });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/feedback/Avatar.jsx", error: String((e && e.message) || e) }); }

// components/feedback/CountBadge.jsx
try { (() => {
/** CountBadge — muted rounded count chip (Database section headers). */
function CountBadge({
  children
}) {
  return /*#__PURE__*/React.createElement("span", {
    style: {
      font: '700 10px var(--font-sans)',
      color: 'var(--text-faint)',
      background: 'var(--neutral-bg)',
      padding: '2px 9px',
      borderRadius: 'var(--radius-pill)'
    }
  }, children);
}
Object.assign(__ds_scope, { CountBadge });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/feedback/CountBadge.jsx", error: String((e && e.message) || e) }); }

// components/feedback/LaborBadge.jsx
try { (() => {
/** LaborBadge — small tinted pill for a staff member's labor category (ENG I, ENG II…). */
function LaborBadge({
  children
}) {
  return /*#__PURE__*/React.createElement("span", {
    style: {
      font: '700 10px var(--font-sans)',
      color: 'var(--primary-hex)',
      background: 'var(--success-bg-strong)',
      padding: '2px 9px',
      borderRadius: 'var(--radius-sm)'
    }
  }, children);
}
Object.assign(__ds_scope, { LaborBadge });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/feedback/LaborBadge.jsx", error: String((e && e.message) || e) }); }

// components/feedback/LevelBadge.jsx
try { (() => {
/** LevelBadge — solid pill used for curriculum-level codes ("100 LEVEL"). */
function LevelBadge({
  children
}) {
  return /*#__PURE__*/React.createElement("span", {
    style: {
      font: '800 12px var(--font-sans)',
      color: '#fff',
      background: 'var(--primary-hex)',
      padding: '5px 11px',
      borderRadius: 'var(--radius-md)'
    }
  }, children);
}
Object.assign(__ds_scope, { LevelBadge });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/feedback/LevelBadge.jsx", error: String((e && e.message) || e) }); }

// components/feedback/ProficiencyChip.jsx
try { (() => {
const PROFICIENCY = [{
  label: 'None',
  bg: 'var(--prof-none-bg)',
  bd: 'var(--prof-none-border)',
  tc: 'var(--prof-none-ink)'
}, {
  label: 'Learning',
  bg: 'var(--prof-learning-bg)',
  bd: 'var(--prof-learning-border)',
  tc: 'var(--prof-learning-ink)'
}, {
  label: 'Proficient',
  bg: 'var(--prof-proficient-bg)',
  bd: 'var(--prof-proficient-border)',
  tc: 'var(--prof-proficient-ink)'
}, {
  label: 'Expert',
  bg: 'var(--prof-expert-bg)',
  bd: 'var(--prof-expert-border)',
  tc: 'var(--prof-expert-ink)'
}];

/** ProficiencyChip — 4-step skill-rating chip (None/Learning/Proficient/Expert), cycles on click. Copied from SkillsView. */
function ProficiencyChip({
  level = 0,
  onClick
}) {
  const p = PROFICIENCY[level] || PROFICIENCY[0];
  return /*#__PURE__*/React.createElement("button", {
    onClick: onClick,
    style: {
      width: '100%',
      maxWidth: 120,
      cursor: 'pointer',
      font: '600 11px var(--font-sans)',
      padding: '5px 8px',
      borderRadius: 'var(--radius-sm)',
      border: `1px solid ${p.bd}`,
      borderStyle: level === 0 ? 'dashed' : 'solid',
      color: p.tc,
      background: p.bg
    }
  }, level === 0 ? '—' : p.label);
}
const SKILL_PROFICIENCY = PROFICIENCY;
Object.assign(__ds_scope, { ProficiencyChip, SKILL_PROFICIENCY });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/feedback/ProficiencyChip.jsx", error: String((e && e.message) || e) }); }

// components/feedback/ProgressBar.jsx
try { (() => {
/** ProgressBar — track + fill + percentage label. Copied from AssignmentsView .progressRow. */
function ProgressBar({
  ratio = 0
}) {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 10
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      flex: 1,
      height: 6,
      background: 'var(--progress-track)',
      borderRadius: 'var(--radius-pill)',
      overflow: 'hidden'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      height: '100%',
      background: 'var(--primary-hex)',
      borderRadius: 'var(--radius-pill)',
      transformOrigin: 'left',
      transform: `scaleX(${ratio})`,
      transition: 'transform 0.6s var(--ease-overshoot)'
    }
  })), /*#__PURE__*/React.createElement("span", {
    style: {
      font: '700 11px var(--font-sans)',
      color: 'var(--primary-hex)',
      width: 34,
      textAlign: 'right'
    }
  }, Math.round(ratio * 100), "%"));
}
Object.assign(__ds_scope, { ProgressBar });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/feedback/ProgressBar.jsx", error: String((e && e.message) || e) }); }

// components/feedback/StatusPill.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
const STATUS = {
  done: {
    label: 'Complete',
    c: 'var(--success-ink)',
    bg: 'var(--success-bg)',
    bd: 'var(--success-border)'
  },
  prog: {
    label: 'In Progress',
    c: 'var(--warning-ink)',
    bg: 'var(--warning-bg)',
    bd: 'var(--warning-border)'
  },
  not: {
    label: 'Not Started',
    c: 'var(--neutral-ink)',
    bg: 'var(--neutral-bg)',
    bd: 'var(--neutral-border)'
  },
  available: {
    label: 'Available',
    c: 'var(--success-ink)',
    bg: '#e1eee6',
    bd: 'var(--success-border)'
  },
  unavailable: {
    label: 'Unavailable',
    c: 'var(--danger-ink)',
    bg: 'var(--danger-bg)',
    bd: 'var(--danger-border)'
  }
};

/**
 * StatusPill — pill-shaped status label (assignment status, availability).
 * Copied from helpers.ts STATUS_META + CurriculumView .availBtn.
 */
function StatusPill({
  status = 'not',
  style,
  ...rest
}) {
  const m = STATUS[status] || STATUS.not;
  return /*#__PURE__*/React.createElement("button", _extends({}, rest, {
    style: {
      cursor: 'pointer',
      font: '600 11px var(--font-sans)',
      padding: '5px 13px',
      borderRadius: 'var(--radius-pill)',
      border: `1px solid ${m.bd}`,
      color: m.c,
      background: m.bg,
      ...style
    }
  }), m.label);
}
Object.assign(__ds_scope, { StatusPill });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/feedback/StatusPill.jsx", error: String((e && e.message) || e) }); }

// components/forms/Button.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
const VARIANT_STYLE = {
  primary: {
    border: '1px solid var(--primary-hex)',
    background: 'var(--primary-hex)',
    color: '#fff'
  },
  secondary: {
    border: '1px solid #cfc7b0',
    background: '#fff',
    color: '#5c6660'
  },
  soft: {
    border: '1px solid #c6d6c9',
    background: '#eff5f0',
    color: 'var(--primary-hex)'
  },
  dashed: {
    border: '1px dashed #cfc7b0',
    background: 'transparent',
    color: '#8a8570'
  },
  danger: {
    border: '1px solid #ead9d3',
    background: '#fbf1ee',
    color: 'var(--danger-ink)'
  }
};
const SIZE_STYLE = {
  sm: {
    padding: '6px 12px',
    fontSize: 11
  },
  md: {
    padding: '9px 15px',
    fontSize: '12.5px'
  },
  lg: {
    padding: '9px 20px',
    fontSize: 13
  }
};

/**
 * Button — toolbar / footer action button. Variants and sizing copied
 * from Header .toolbarBtn(Primary), CurriculumView .footBtn family, and
 * DatabaseView .addBtn(Solid).
 */
function Button({
  variant = 'secondary',
  size = 'md',
  children,
  style,
  ...rest
}) {
  const v = VARIANT_STYLE[variant] || VARIANT_STYLE.secondary;
  const s = SIZE_STYLE[size] || SIZE_STYLE.md;
  return /*#__PURE__*/React.createElement("button", _extends({}, rest, {
    style: {
      cursor: 'pointer',
      fontFamily: 'var(--font-sans)',
      fontWeight: 600,
      borderRadius: 'var(--radius-md)',
      whiteSpace: 'nowrap',
      transition: 'transform var(--duration-hover) var(--ease-overshoot), box-shadow var(--duration-base) ease, background var(--duration-base) ease, border-color var(--duration-base) ease',
      ...v,
      ...s,
      ...style
    },
    onMouseEnter: e => {
      e.currentTarget.style.transform = 'translateY(-1px)';
      rest.onMouseEnter && rest.onMouseEnter(e);
    },
    onMouseLeave: e => {
      e.currentTarget.style.transform = 'translateY(0)';
      rest.onMouseLeave && rest.onMouseLeave(e);
    }
  }), children);
}
Object.assign(__ds_scope, { Button });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/forms/Button.jsx", error: String((e && e.message) || e) }); }

// components/forms/IconButton.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * IconButton — small icon-only control for delete (✕) and close affordances.
 * The source app renders these as literal "✕" text glyphs (Modal close,
 * row-level delete buttons) rather than SVG icons — reproduced verbatim.
 */
function IconButton({
  tone = 'default',
  size = 14,
  title,
  children = '\u2715',
  style,
  ...rest
}) {
  const toneColor = tone === 'danger-hover' ? '#c7bfa8' : tone === 'muted' ? '#a7a18c' : '#c7bfa8';
  return /*#__PURE__*/React.createElement("button", _extends({
    title: title
  }, rest, {
    style: {
      cursor: 'pointer',
      border: 'none',
      background: 'transparent',
      color: toneColor,
      fontFamily: 'var(--font-sans)',
      fontWeight: 600,
      fontSize: size,
      padding: '2px 6px',
      transition: 'color 0.15s ease',
      ...style
    },
    onMouseEnter: e => {
      e.currentTarget.style.color = 'var(--danger-ink)';
    },
    onMouseLeave: e => {
      e.currentTarget.style.color = toneColor;
    }
  }), children);
}
Object.assign(__ds_scope, { IconButton });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/forms/IconButton.jsx", error: String((e && e.message) || e) }); }

// components/forms/InlineEditText.jsx
try { (() => {
const {
  useEffect,
  useRef,
  useState
} = React;
/**
 * InlineEditText — click text to turn it into an input, commit on blur/Enter,
 * cancel on Escape. Copied from InlineEditText.tsx. Used for course/lesson
 * titles throughout Curriculum.
 */
function InlineEditText({
  value,
  onCommit,
  style,
  inputStyle,
  title,
  placeholder
}) {
  const [editing, setEditing] = useState(false);
  const [draft, setDraft] = useState(value);
  const ref = useRef(null);
  useEffect(() => {
    if (editing) {
      setDraft(value);
      requestAnimationFrame(() => {
        ref.current && ref.current.focus();
        ref.current && ref.current.select();
      });
    }
  }, [editing]);
  function commit() {
    setEditing(false);
    if (draft.trim() && draft !== value) onCommit(draft.trim());
  }
  function cancel() {
    setEditing(false);
    setDraft(value);
  }
  if (editing) {
    return /*#__PURE__*/React.createElement("input", {
      ref: ref,
      value: draft,
      placeholder: placeholder,
      onChange: e => setDraft(e.target.value),
      onClick: e => e.stopPropagation(),
      onMouseDown: e => e.stopPropagation(),
      onBlur: commit,
      onKeyDown: e => {
        if (e.key === 'Enter') commit();
        if (e.key === 'Escape') cancel();
      },
      style: {
        display: 'block',
        width: '100%',
        border: 'none',
        borderBottom: '1.5px solid var(--gold-line)',
        background: 'var(--gold-surface)',
        outline: 'none',
        padding: '1px 3px',
        borderRadius: '4px 4px 0 0',
        font: 'inherit',
        color: 'inherit',
        ...inputStyle
      }
    });
  }
  return /*#__PURE__*/React.createElement("span", {
    style: {
      borderRadius: 4,
      padding: '1px 3px',
      margin: '0 -3px',
      cursor: 'pointer',
      transition: 'background 0.15s ease',
      ...style
    },
    title: title || 'Click to rename',
    onClick: e => {
      e.stopPropagation();
      setEditing(true);
    },
    onMouseEnter: e => {
      e.currentTarget.style.background = '#f3eee1';
    },
    onMouseLeave: e => {
      e.currentTarget.style.background = 'transparent';
    }
  }, value);
}
Object.assign(__ds_scope, { InlineEditText });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/forms/InlineEditText.jsx", error: String((e && e.message) || e) }); }

// components/forms/Input.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/** Text input — copied from Modal .fieldInput / DatabaseView .input (7–11px vertical padding, 1px hairline border). */
function Input({
  style,
  ...rest
}) {
  return /*#__PURE__*/React.createElement("input", _extends({}, rest, {
    style: {
      width: '100%',
      padding: '10px 12px',
      border: '1px solid var(--line-input-2)',
      borderRadius: 'var(--radius-lg)',
      font: '500 13px var(--font-sans)',
      color: 'var(--text-body)',
      background: '#fff',
      ...style
    }
  }));
}

/** Select dropdown — same visual treatment as Input. */
function Select({
  style,
  children,
  ...rest
}) {
  return /*#__PURE__*/React.createElement("select", _extends({}, rest, {
    style: {
      width: '100%',
      padding: '10px 12px',
      border: '1px solid var(--line-input-2)',
      borderRadius: 'var(--radius-lg)',
      font: '500 13px var(--font-sans)',
      color: 'var(--text-body)',
      background: '#fff',
      cursor: 'pointer',
      ...style
    }
  }), children);
}

/** Field label wrapper — uppercase 11px label above an Input/Select, per Modal .fieldLabel. */
function FormField({
  label,
  children
}) {
  return /*#__PURE__*/React.createElement("label", {
    style: {
      display: 'block'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      display: 'block',
      font: '600 11px var(--font-sans)',
      letterSpacing: '0.03em',
      textTransform: 'uppercase',
      color: 'var(--text-faint)',
      marginBottom: 6
    }
  }, label), children);
}
Object.assign(__ds_scope, { Input, Select, FormField });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/forms/Input.jsx", error: String((e && e.message) || e) }); }

// components/icons/Icon.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Stroke-icon glyph set copied verbatim from the source app (inline SVG
 * paths used in Sidebar nav, resource-type chips, chevrons, etc — the app
 * has no icon font or sprite sheet, just hand-authored 24x24 stroke paths).
 * Default stroke width 1.9–2.4 with round caps/joins, per source usage.
 */
const PATHS = {
  curriculum: 'M4 5h16v14H4zM4 9h16M9 9v10',
  assignments: 'M9 5h6M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 00-2 2v0M7 7H6a2 2 0 00-2 2v9a2 2 0 002 2h12a2 2 0 002-2V9a2 2 0 00-2-2h-1M9 13l2 2 4-4',
  matrix: 'M3 3h18v18H3zM3 9h18M3 15h18M9 3v18M15 3v18',
  skills: 'M12 3l9 5-9 5-9-5zM3 13l9 5 9-5',
  database: 'M4 6c0 1.7 3.6 3 8 3s8-1.3 8-3-3.6-3-8-3-8 1.3-8 3M4 6v6c0 1.7 3.6 3 8 3s8-1.3 8-3V6M4 12v6c0 1.7 3.6 3 8 3s8-1.3 8-3v-6',
  chevronDown: 'M6 9l6 6 6-6',
  chevronRight: 'M9 6l6 6-6 6',
  search: 'M21 21l-4.3-4.3',
  clock: 'M12 7v5l3 2',
  close: 'M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4M16 17l5-5-5-5M21 12H9',
  externalLink: 'M7 17L17 7M9 7h8v8',
  docType: 'M14 3v5h5M7 3h7l5 5v13H7z',
  videoType: 'M8 5v14l11-7z',
  esriType: 'M12 3a9 9 0 100 18 9 9 0 000-18M3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18',
  activityType: 'M17 20v-2a4 4 0 00-4-4H7a4 4 0 00-4 4v2M9 10a3 3 0 100-6 3 3 0 000 6M21 20v-1.5a4 4 0 00-3-3.8',
  quizType: 'M9 12l2 2 4-4M12 3a9 9 0 100 18 9 9 0 000-18',
  linkType: 'M14 3h7v7M21 3l-9 9M10 5H5v14h14v-5'
};
function Icon({
  name,
  size = 16,
  strokeWidth = 2,
  color = 'currentColor',
  style,
  ...rest
}) {
  const d = PATHS[name];
  if (!d) return null;
  return /*#__PURE__*/React.createElement("svg", _extends({
    width: size,
    height: size,
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: color,
    strokeWidth: strokeWidth,
    strokeLinecap: "round",
    strokeLinejoin: "round",
    style: style
  }, rest), /*#__PURE__*/React.createElement("path", {
    d: d
  }));
}

/** Circle-of-dots drag grip, used on draggable Assignment cards. */
function GripIcon({
  size = 10,
  color = 'currentColor'
}) {
  const h = size * 1.6;
  return /*#__PURE__*/React.createElement("svg", {
    width: size,
    height: h,
    viewBox: "0 0 10 16",
    fill: color
  }, /*#__PURE__*/React.createElement("circle", {
    cx: "2.5",
    cy: "2.5",
    r: "1.5"
  }), /*#__PURE__*/React.createElement("circle", {
    cx: "7.5",
    cy: "2.5",
    r: "1.5"
  }), /*#__PURE__*/React.createElement("circle", {
    cx: "2.5",
    cy: "8",
    r: "1.5"
  }), /*#__PURE__*/React.createElement("circle", {
    cx: "7.5",
    cy: "8",
    r: "1.5"
  }), /*#__PURE__*/React.createElement("circle", {
    cx: "2.5",
    cy: "13.5",
    r: "1.5"
  }), /*#__PURE__*/React.createElement("circle", {
    cx: "7.5",
    cy: "13.5",
    r: "1.5"
  }));
}
const ICON_NAMES = Object.keys(PATHS);
Object.assign(__ds_scope, { Icon, GripIcon, ICON_NAMES });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/icons/Icon.jsx", error: String((e && e.message) || e) }); }

// components/data/DisclosureCard.jsx
try { (() => {
/**
 * DisclosureCard — a card with a clickable header (chevron + title + meta)
 * that expands a body. This is the shape shared by Curriculum course cards,
 * Assignment staff cards, and Database sections — copied from their
 * respective .card/.cardHead/.expandOuter treatments (13px vs 16px radius
 * kept as a `radius` prop since the source uses both).
 */
function DisclosureCard({
  open,
  onToggle,
  header,
  children,
  radius = 13,
  elevated = false
}) {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      background: 'var(--card-bg)',
      borderRadius: radius,
      overflow: 'hidden',
      border: elevated ? undefined : '1px solid var(--line-2)',
      boxShadow: elevated ? 'var(--shadow-card)' : undefined
    }
  }, /*#__PURE__*/React.createElement("button", {
    onClick: onToggle,
    style: {
      display: 'flex',
      alignItems: 'flex-start',
      gap: 12,
      width: '100%',
      textAlign: 'left',
      cursor: 'pointer',
      padding: '15px 16px',
      border: 'none',
      background: elevated ? '#fbfaf5' : 'transparent',
      borderBottom: elevated ? '1px solid var(--line)' : 'none'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      flex: 1,
      minWidth: 0
    }
  }, header), /*#__PURE__*/React.createElement(__ds_scope.Icon, {
    name: "chevronDown",
    size: 17,
    strokeWidth: 2,
    color: "#B7B29A",
    style: {
      flex: 'none',
      marginTop: 2,
      transition: 'transform 0.2s',
      transform: `rotate(${open ? 180 : 0}deg)`
    }
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'grid',
      gridTemplateRows: open ? '1fr' : '0fr',
      transition: 'grid-template-rows 0.34s var(--ease-standard)'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      overflow: 'hidden',
      minHeight: 0
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      padding: '2px 16px 14px',
      borderTop: '1px solid var(--line)'
    }
  }, children))));
}
Object.assign(__ds_scope, { DisclosureCard });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/data/DisclosureCard.jsx", error: String((e && e.message) || e) }); }

// components/data/ResourceRow.jsx
try { (() => {
const RES_META = {
  video: {
    c: 'var(--icon-video-ink)',
    bg: 'var(--icon-video-bg)',
    icon: 'videoType',
    label: 'Video'
  },
  doc: {
    c: 'var(--icon-doc-ink)',
    bg: 'var(--icon-doc-bg)',
    icon: 'docType',
    label: 'Document'
  },
  esri: {
    c: 'var(--icon-esri-ink)',
    bg: 'var(--icon-esri-bg)',
    icon: 'esriType',
    label: 'External Training'
  },
  activity: {
    c: 'var(--icon-activity-ink)',
    bg: 'var(--icon-activity-bg)',
    icon: 'activityType',
    label: 'In-Person'
  },
  quiz: {
    c: 'var(--icon-quiz-ink)',
    bg: 'var(--icon-quiz-bg)',
    icon: 'quizType',
    label: 'Quiz'
  },
  link: {
    c: 'var(--icon-default-ink)',
    bg: 'var(--icon-default-bg)',
    icon: 'linkType',
    label: 'Link'
  }
};
function resourceMeta(type) {
  return RES_META[type] || RES_META.link;
}

/**
 * ResourceRow — a lesson resource (doc/video/link/…): tinted icon chip,
 * title + type/source meta. Copied from CurriculumView .resourceRow.
 */
function ResourceRow({
  type = 'doc',
  title,
  meta,
  href,
  onClick
}) {
  const m = resourceMeta(type);
  const Tag = href ? 'a' : 'div';
  return /*#__PURE__*/React.createElement(Tag, {
    href: href,
    target: href ? '_blank' : undefined,
    rel: href ? 'noreferrer' : undefined,
    onClick: onClick,
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 10,
      padding: '7px 10px',
      border: '1px solid var(--line-3)',
      borderRadius: 'var(--radius-lg)',
      marginBottom: 6,
      background: '#fdfcf8',
      textDecoration: 'none',
      cursor: onClick ? 'pointer' : href ? 'pointer' : 'default'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      flex: 'none',
      width: 26,
      height: 26,
      borderRadius: 'var(--radius-sm)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      background: m.bg,
      color: m.c
    }
  }, /*#__PURE__*/React.createElement(__ds_scope.Icon, {
    name: m.icon,
    size: 13,
    strokeWidth: 1.9
  })), /*#__PURE__*/React.createElement("span", {
    style: {
      flex: 1,
      minWidth: 0
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      display: 'block',
      font: '600 12px/1.2 var(--font-sans)',
      color: '#33403a'
    }
  }, title), /*#__PURE__*/React.createElement("span", {
    style: {
      display: 'block',
      font: '500 10.5px var(--font-sans)',
      color: 'var(--text-faint-2)'
    }
  }, m.label, meta ? ` · ${meta}` : '')), href && /*#__PURE__*/React.createElement(__ds_scope.Icon, {
    name: "externalLink",
    size: 13,
    strokeWidth: 2,
    color: "#B7B29A"
  }));
}
Object.assign(__ds_scope, { resourceMeta, ResourceRow });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/data/ResourceRow.jsx", error: String((e && e.message) || e) }); }

// components/forms/SearchBar.jsx
try { (() => {
/** Search input with leading search icon and a clear (✕) button — copied from SearchBar.tsx. */
function SearchBar({
  value,
  onChange,
  placeholder
}) {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'relative',
      marginBottom: 22,
      maxWidth: 420
    }
  }, /*#__PURE__*/React.createElement(__ds_scope.Icon, {
    name: "search",
    size: 16,
    strokeWidth: 2,
    color: "#A7A18C",
    style: {
      position: 'absolute',
      left: 13,
      top: '50%',
      transform: 'translateY(-50%)'
    }
  }), /*#__PURE__*/React.createElement("input", {
    value: value,
    onChange: e => onChange(e.target.value),
    placeholder: placeholder,
    style: {
      width: '100%',
      padding: '10px 14px 10px 38px',
      border: '1px solid var(--line-input)',
      borderRadius: 'var(--radius-lg)',
      font: '500 13px var(--font-sans)',
      color: 'var(--text-body)',
      background: '#fff'
    }
  }), value && /*#__PURE__*/React.createElement("button", {
    onClick: () => onChange(''),
    style: {
      position: 'absolute',
      right: 8,
      top: '50%',
      transform: 'translateY(-50%)',
      cursor: 'pointer',
      border: 'none',
      background: 'transparent',
      color: '#a7a18c',
      font: '600 15px var(--font-sans)',
      padding: '4px 6px'
    }
  }, "\u2715"));
}

/** Empty-search-results message — copied from SearchBar.tsx NoResults. */
function NoResults({
  query
}) {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      padding: '40px 20px',
      textAlign: 'center',
      font: '500 13px var(--font-sans)',
      color: '#9a957f'
    }
  }, "No matches for \u201C", query, "\u201D.");
}
Object.assign(__ds_scope, { SearchBar, NoResults });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/forms/SearchBar.jsx", error: String((e && e.message) || e) }); }

// components/layout/Header.jsx
try { (() => {
/**
 * Header — sticky page header with an overline + serif title on the left,
 * and toolbar buttons on the right, plus a faint decorative wave line motif.
 * Copied from Header.tsx/.module.css.
 */
function Header({
  title,
  toolbar = []
}) {
  return /*#__PURE__*/React.createElement("header", {
    style: {
      position: 'sticky',
      top: 0,
      zIndex: 20,
      overflow: 'hidden',
      background: 'oklch(0.975 0.008 96 / 0.97)',
      backdropFilter: 'var(--blur-glass)',
      WebkitBackdropFilter: 'var(--blur-glass)',
      borderBottom: '1px solid var(--border)',
      boxShadow: '0 1px 0 var(--border-soft), 0 6px 20px -14px oklch(0.3 0.05 150 / 0.35)',
      padding: '24px 40px'
    }
  }, /*#__PURE__*/React.createElement("svg", {
    viewBox: "0 0 340 120",
    preserveAspectRatio: "xMaxYMid slice",
    fill: "none",
    stroke: "#DDE9DF",
    strokeWidth: "1.2",
    style: {
      position: 'absolute',
      right: 0,
      top: 0,
      height: '100%',
      width: 340,
      opacity: 0.5
    }
  }, /*#__PURE__*/React.createElement("path", {
    d: "M-10 30 C60 8,120 52,190 34 S320 8,360 34"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M-10 58 C60 36,120 80,190 62 S320 36,360 62"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M-10 86 C60 64,120 108,190 90 S320 64,360 90"
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'relative',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      gap: 16
    }
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    style: {
      font: '600 10px var(--font-sans)',
      letterSpacing: '0.15em',
      textTransform: 'uppercase',
      color: '#7ba98c',
      marginBottom: 6
    }
  }, "Water Resources"), /*#__PURE__*/React.createElement("h1", {
    style: {
      font: '600 26px/1.1 var(--font-serif)',
      color: 'var(--text-heading)'
    }
  }, title)), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      gap: 10,
      flexWrap: 'wrap',
      justifyContent: 'flex-end'
    }
  }, toolbar.map(b => /*#__PURE__*/React.createElement("button", {
    key: b.label,
    onClick: b.onClick,
    style: {
      cursor: 'pointer',
      transition: 'transform 0.16s var(--ease-overshoot), box-shadow 0.18s ease, background 0.18s ease, border-color 0.18s ease',
      border: b.primary ? '1px solid var(--primary-hex)' : '1px solid #cfc7b0',
      background: b.primary ? 'var(--primary-hex)' : '#fff',
      color: b.primary ? '#fff' : '#5c6660',
      font: '600 12.5px var(--font-sans)',
      padding: '9px 15px',
      borderRadius: 'var(--radius-md)'
    },
    onMouseEnter: e => {
      e.currentTarget.style.transform = 'translateY(-1px)';
    },
    onMouseLeave: e => {
      e.currentTarget.style.transform = 'translateY(0)';
    }
  }, b.label)))));
}
Object.assign(__ds_scope, { Header });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/layout/Header.jsx", error: String((e && e.message) || e) }); }

// components/layout/Logo.jsx
try { (() => {
/**
 * Logo — the GHA Water Resources mark: a water droplet with two ripple
 * lines, inline SVG (no raster/logo file dependency). Copied verbatim
 * from Logo.tsx / favicon.svg.
 */
function Logo({
  size = 34
}) {
  return /*#__PURE__*/React.createElement("svg", {
    width: size,
    height: size,
    viewBox: "0 0 32 32",
    fill: "none"
  }, /*#__PURE__*/React.createElement("path", {
    d: "M16 3C16 3 7 13 7 20a9 9 0 0018 0C25 13 16 3 16 3Z",
    fill: "#2F6B4C"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M10.6 20c1.6 1.8 3.2 1.8 4.8 0s3.2-1.8 4.8 0",
    stroke: "#EAF2EB",
    strokeWidth: "1.5",
    fill: "none",
    strokeLinecap: "round"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M10.6 16c1.6 1.8 3.2 1.8 4.8 0s3.2-1.8 4.8 0",
    stroke: "#9FD0AE",
    strokeWidth: "1.4",
    fill: "none",
    strokeLinecap: "round",
    opacity: ".85"
  }));
}
Object.assign(__ds_scope, { Logo });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/layout/Logo.jsx", error: String((e && e.message) || e) }); }

// components/layout/PageContent.jsx
try { (() => {
/** PageContent — max-width content wrapper with page padding. Copied from PageContent.tsx. */
function PageContent({
  children
}) {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      padding: '26px 40px 60px',
      maxWidth: 1240,
      width: '100%'
    }
  }, children);
}
Object.assign(__ds_scope, { PageContent });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/layout/PageContent.jsx", error: String((e && e.message) || e) }); }

// components/layout/Sidebar.jsx
try { (() => {
const NAV = [{
  id: 'curriculum',
  label: 'Curriculum',
  icon: 'curriculum'
}, {
  id: 'assignments',
  label: 'Assignments',
  icon: 'assignments'
}, {
  id: 'matrix',
  label: 'Training Matrix',
  icon: 'matrix'
}, {
  id: 'skills',
  label: 'Skills & Experience',
  icon: 'skills'
}, {
  id: 'database',
  label: 'Database',
  icon: 'database'
}];

/**
 * Sidebar — fixed-width glass nav rail: brand mark + name, nav list with
 * active-state left accent, and a footer with the signed-in user + sign out.
 * Copied from Sidebar.tsx/.module.css.
 */
function Sidebar({
  view,
  onSelect,
  userName = 'you@ghauniversity.org',
  onSignOut
}) {
  return /*#__PURE__*/React.createElement("aside", {
    style: {
      width: 250,
      flex: 'none',
      background: 'var(--glass)',
      backdropFilter: 'var(--blur-glass)',
      WebkitBackdropFilter: 'var(--blur-glass)',
      borderRight: '1px solid var(--glass-line)',
      boxShadow: '1px 0 0 var(--border-soft)',
      display: 'flex',
      flexDirection: 'column',
      position: 'sticky',
      top: 0,
      height: '100vh',
      zIndex: 10
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      padding: '22px 20px 18px',
      borderBottom: '1px solid var(--line)'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 12
    }
  }, /*#__PURE__*/React.createElement(__ds_scope.Logo, {
    size: 34
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      lineHeight: 1.1
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      font: '800 15px var(--font-sans)',
      color: 'var(--text-heading)',
      letterSpacing: '0.01em',
      whiteSpace: 'nowrap'
    }
  }, "GHA University"), /*#__PURE__*/React.createElement("div", {
    style: {
      font: '600 9px var(--font-sans)',
      letterSpacing: '0.15em',
      textTransform: 'uppercase',
      color: '#7ba98c',
      marginTop: 2
    }
  }, "Water Resources")))), /*#__PURE__*/React.createElement("nav", {
    style: {
      padding: '14px 12px',
      flex: 1
    }
  }, NAV.map(n => {
    const active = view === n.id;
    return /*#__PURE__*/React.createElement("button", {
      key: n.id,
      onClick: () => onSelect(n.id),
      style: {
        display: 'flex',
        alignItems: 'center',
        gap: 12,
        width: '100%',
        cursor: 'pointer',
        border: 'none',
        borderRadius: 'var(--radius-lg)',
        padding: '10px 12px',
        marginBottom: 2,
        font: active ? '600 13px var(--font-sans)' : '500 13px var(--font-sans)',
        color: active ? 'var(--text-heading)' : '#5c6660',
        background: active ? 'var(--sidebar-active-bg)' : 'transparent',
        boxShadow: active ? 'inset 3px 0 0 var(--primary-hex)' : 'none',
        transition: 'transform 0.2s var(--ease-overshoot-lg), background 0.18s ease'
      },
      onMouseEnter: e => {
        e.currentTarget.style.transform = 'translateX(3px)';
      },
      onMouseLeave: e => {
        e.currentTarget.style.transform = 'translateX(0)';
      }
    }, /*#__PURE__*/React.createElement(__ds_scope.Icon, {
      name: n.icon,
      size: 17,
      strokeWidth: 1.9
    }), /*#__PURE__*/React.createElement("span", {
      style: {
        flex: 1,
        textAlign: 'left'
      }
    }, n.label));
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      padding: '14px 16px',
      borderTop: '1px solid var(--line)',
      display: 'flex',
      alignItems: 'center',
      gap: 10
    }
  }, /*#__PURE__*/React.createElement(__ds_scope.Avatar, {
    name: userName.split('@')[0],
    size: 30
  }), /*#__PURE__*/React.createElement("span", {
    style: {
      flex: 1,
      minWidth: 0,
      overflow: 'hidden'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      display: 'block',
      font: '600 11.5px var(--font-sans)',
      color: '#33403a',
      whiteSpace: 'nowrap',
      overflow: 'hidden',
      textOverflow: 'ellipsis'
    }
  }, userName)), /*#__PURE__*/React.createElement("button", {
    title: "Sign out",
    onClick: onSignOut,
    style: {
      cursor: 'pointer',
      border: 'none',
      background: 'transparent',
      color: '#b7b29a',
      display: 'flex',
      padding: 4
    }
  }, /*#__PURE__*/React.createElement("svg", {
    width: "16",
    height: "16",
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "currentColor",
    strokeWidth: "2",
    strokeLinecap: "round",
    strokeLinejoin: "round"
  }, /*#__PURE__*/React.createElement("path", {
    d: "M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4M16 17l5-5-5-5M21 12H9"
  })))));
}
Object.assign(__ds_scope, { Sidebar });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/layout/Sidebar.jsx", error: String((e && e.message) || e) }); }

// components/overlay/Modal.jsx
try { (() => {
const {
  useEffect,
  useState
} = React;
/**
 * Modal — centered dialog shell (backdrop + white card, 16px radius,
 * fixed-width 440px) plus the Confirm and Form body variants. Copied
 * from Modal.tsx/.module.css (framer-motion entrance simplified to a
 * CSS transition here to keep the component dependency-free).
 */
function Modal({
  open,
  onClose,
  children
}) {
  if (!open) return null;
  return /*#__PURE__*/React.createElement("div", {
    onClick: onClose,
    style: {
      position: 'fixed',
      inset: 0,
      zIndex: 50,
      background: 'rgba(35, 42, 32, 0.42)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: 24
    }
  }, /*#__PURE__*/React.createElement("div", {
    onClick: e => e.stopPropagation(),
    style: {
      background: '#fff',
      borderRadius: 16,
      width: 440,
      maxWidth: '100%',
      maxHeight: '86vh',
      overflow: 'auto',
      boxShadow: 'var(--shadow-modal)',
      animation: 'cardIn 0.22s var(--ease-entrance) both'
    }
  }, children));
}
function ModalHead({
  title,
  onClose
}) {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      padding: '18px 22px',
      borderBottom: '1px solid var(--line)'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      font: '700 15px var(--font-serif)',
      color: 'var(--text-heading)'
    }
  }, title), /*#__PURE__*/React.createElement("button", {
    onClick: onClose,
    style: {
      cursor: 'pointer',
      border: 'none',
      background: 'transparent',
      color: '#a7a18c',
      font: '600 17px var(--font-sans)'
    }
  }, "\u2715"));
}
function ModalBody({
  children
}) {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      padding: '20px 22px'
    }
  }, children);
}
function ModalFoot({
  children
}) {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      justifyContent: 'flex-end',
      gap: 10,
      padding: '16px 22px',
      borderTop: '1px solid var(--line)'
    }
  }, children);
}

/** ConfirmModal — title + message + Cancel/Delete. Copied from Modal.tsx ConfirmBody. */
function ConfirmModal({
  open,
  title,
  message,
  saveLabel = 'Delete',
  onCancel,
  onConfirm
}) {
  return /*#__PURE__*/React.createElement(Modal, {
    open: open,
    onClose: onCancel
  }, /*#__PURE__*/React.createElement(ModalHead, {
    title: title,
    onClose: onCancel
  }), /*#__PURE__*/React.createElement(ModalBody, null, /*#__PURE__*/React.createElement("p", {
    style: {
      margin: 0,
      font: '500 13.5px/1.5 var(--font-sans)',
      color: 'var(--text-muted)'
    }
  }, message)), /*#__PURE__*/React.createElement(ModalFoot, null, /*#__PURE__*/React.createElement(CancelButton, {
    onClick: onCancel
  }), /*#__PURE__*/React.createElement(DangerSaveButton, {
    onClick: onConfirm
  }, saveLabel)));
}
function CancelButton({
  onClick
}) {
  return /*#__PURE__*/React.createElement("button", {
    onClick: onClick,
    style: {
      cursor: 'pointer',
      border: '1px solid var(--line-input-2)',
      background: '#fff',
      color: 'var(--text-faint)',
      font: '600 13px var(--font-sans)',
      padding: '9px 18px',
      borderRadius: 9
    }
  }, "Cancel");
}
function PrimarySaveButton({
  onClick,
  children
}) {
  return /*#__PURE__*/React.createElement("button", {
    onClick: onClick,
    style: {
      cursor: 'pointer',
      border: 'none',
      color: '#fff',
      font: '600 13px var(--font-sans)',
      padding: '9px 20px',
      borderRadius: 9,
      background: 'var(--primary-hex)'
    }
  }, children);
}
function DangerSaveButton({
  onClick,
  children
}) {
  return /*#__PURE__*/React.createElement("button", {
    onClick: onClick,
    style: {
      cursor: 'pointer',
      border: 'none',
      color: '#fff',
      font: '600 13px var(--font-sans)',
      padding: '9px 20px',
      borderRadius: 9,
      background: 'var(--danger-ink)'
    }
  }, children);
}
Object.assign(__ds_scope, { Modal, ModalHead, ModalBody, ModalFoot, ConfirmModal, CancelButton, PrimarySaveButton, DangerSaveButton });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/overlay/Modal.jsx", error: String((e && e.message) || e) }); }

// ui_kits/water-resources-lms/App.jsx
try { (() => {
function App() {
  const ns = window.GHAUniversityWaterResourcesDesignSystem_a1ef01;
  const {
    Sidebar
  } = ns;
  const [session, setSession] = React.useState(null);
  const [view, setView] = React.useState('curriculum');
  const [db, setDb] = React.useState(window.SEED_DATA);
  function signIn(email) {
    setSession({
      email
    });
  }
  function signOut() {
    setSession(null);
  }
  function onEditCourseTitle(courseId, title) {
    setDb(d => ({
      ...d,
      courses: d.courses.map(c => c.id === courseId ? {
        ...c,
        title
      } : c)
    }));
  }
  function onEditLessonTitle(lessonId, title) {
    setDb(d => ({
      ...d,
      courses: d.courses.map(c => ({
        ...c,
        lessons: c.lessons.map(l => l.id === lessonId ? {
          ...l,
          title
        } : l)
      }))
    }));
  }
  function onToggleAvailable(lessonId) {
    setDb(d => ({
      ...d,
      courses: d.courses.map(c => ({
        ...c,
        lessons: c.lessons.map(l => l.id === lessonId ? {
          ...l,
          available: l.available === false
        } : l)
      }))
    }));
  }
  function onToggleProgress(staffId, lessonId) {
    setDb(d => {
      const key = staffId + '|' + lessonId;
      const next = {
        ...d.lessonProgress
      };
      if (next[key]) delete next[key];else next[key] = true;
      return {
        ...d,
        lessonProgress: next
      };
    });
  }
  function onCycleRating(staffId, skillId) {
    setDb(d => {
      const key = staffId + '|' + skillId;
      const cur = d.skillRatings[key] ?? 0;
      return {
        ...d,
        skillRatings: {
          ...d.skillRatings,
          [key]: (cur + 1) % 4
        }
      };
    });
  }
  if (!session) {
    return /*#__PURE__*/React.createElement(window.LoginScreen, {
      onSignIn: signIn
    });
  }
  const screenProps = {
    db,
    onEditCourseTitle,
    onEditLessonTitle,
    onToggleAvailable,
    onToggleProgress,
    onCycleRating
  };
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      minHeight: '100vh'
    }
  }, /*#__PURE__*/React.createElement(Sidebar, {
    view: view,
    onSelect: setView,
    userName: session.email,
    onSignOut: signOut
  }), /*#__PURE__*/React.createElement("main", {
    style: {
      flex: 1,
      minWidth: 0,
      display: 'flex',
      flexDirection: 'column'
    }
  }, view === 'curriculum' && /*#__PURE__*/React.createElement(window.CurriculumScreen, screenProps), view === 'assignments' && /*#__PURE__*/React.createElement(window.AssignmentsScreen, screenProps), view === 'matrix' && /*#__PURE__*/React.createElement(window.MatrixScreen, screenProps), view === 'skills' && /*#__PURE__*/React.createElement(window.SkillsScreen, screenProps), view === 'database' && /*#__PURE__*/React.createElement(window.DatabaseScreen, screenProps)));
}
ReactDOM.createRoot(document.getElementById('root')).render(/*#__PURE__*/React.createElement(App, null));
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/water-resources-lms/App.jsx", error: String((e && e.message) || e) }); }

// ui_kits/water-resources-lms/AssignmentsScreen.jsx
try { (() => {
function AssignmentsScreen({
  db,
  onToggleProgress
}) {
  const ns = window.GHAUniversityWaterResourcesDesignSystem_a1ef01;
  const {
    Header,
    PageContent,
    SearchBar,
    NoResults,
    DisclosureCard,
    Avatar,
    LaborBadge,
    ProgressBar,
    IconButton,
    GripIcon,
    Icon,
    Button
  } = ns;
  const {
    fmtMin,
    lcCode
  } = window.LmsHelpers;
  const [query, setQuery] = React.useState('');
  const [openIds, setOpenIds] = React.useState({});
  const q = query.toLowerCase().trim();
  const people = db.staff.filter(s => !q || s.name.toLowerCase().includes(q) || lcCode(db, s).toLowerCase().includes(q));
  const noResults = q.length > 0 && people.length === 0;
  function assignedProg(staffId, course) {
    const al = course.lessons.filter(l => !!db.lessonAssign[staffId + '|' + l.id]);
    const done = al.filter(l => !!db.lessonProgress[staffId + '|' + l.id]).length;
    return {
      total: al.length,
      done,
      lessons: al
    };
  }
  return /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement(Header, {
    title: "Training Assignments",
    toolbar: [{
      label: 'Labor categories'
    }, {
      label: '+ Add staff',
      primary: true
    }]
  }), /*#__PURE__*/React.createElement(PageContent, null, /*#__PURE__*/React.createElement(SearchBar, {
    value: query,
    onChange: setQuery,
    placeholder: "Search staff\u2026"
  }), noResults ? /*#__PURE__*/React.createElement(NoResults, {
    query: query
  }) : /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      flexDirection: 'column',
      gap: 16
    }
  }, people.map(s => {
    const rows = db.courses.map(co => ({
      co,
      ap: assignedProg(s.id, co)
    })).filter(x => x.ap.total > 0);
    const totalLessons = rows.reduce((n, x) => n + x.ap.total, 0);
    const doneLessons = rows.reduce((n, x) => n + x.ap.done, 0);
    const coursesDone = rows.filter(x => x.ap.total > 0 && x.ap.done === x.ap.total).length;
    const ratio = totalLessons ? doneLessons / totalLessons : 0;
    return /*#__PURE__*/React.createElement("div", {
      key: s.id,
      style: {
        background: 'var(--surface)',
        borderRadius: 16,
        boxShadow: 'var(--shadow-card)',
        overflow: 'hidden',
        border: '1px solid var(--border)'
      }
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        padding: '14px 20px',
        background: 'var(--head-strip-bg)',
        borderBottom: '1px solid var(--line)'
      }
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        display: 'flex',
        alignItems: 'center',
        gap: 12
      }
    }, /*#__PURE__*/React.createElement("span", {
      style: {
        flex: 'none',
        color: '#cdc6b1'
      }
    }, /*#__PURE__*/React.createElement(GripIcon, {
      size: 10
    })), /*#__PURE__*/React.createElement(Avatar, {
      name: s.name,
      size: 36
    }), /*#__PURE__*/React.createElement("span", {
      style: {
        flex: 1,
        display: 'flex',
        alignItems: 'center',
        gap: 10
      }
    }, /*#__PURE__*/React.createElement("span", {
      style: {
        font: '600 14px var(--font-sans)',
        color: '#2b332e'
      }
    }, s.name), /*#__PURE__*/React.createElement(LaborBadge, null, lcCode(db, s))), /*#__PURE__*/React.createElement("span", {
      style: {
        font: '600 12px var(--font-sans)',
        color: 'var(--text-faint)'
      }
    }, coursesDone, " of ", rows.length, " courses \xB7 ", doneLessons, "/", totalLessons, " lessons"), /*#__PURE__*/React.createElement(IconButton, {
      title: "Remove staff member"
    })), /*#__PURE__*/React.createElement("div", {
      style: {
        marginTop: 11
      }
    }, /*#__PURE__*/React.createElement(ProgressBar, {
      ratio: ratio
    }))), /*#__PURE__*/React.createElement("div", null, rows.map(({
      co,
      ap
    }) => {
      const allDone = ap.total > 0 && ap.done === ap.total;
      const okey = s.id + '|' + co.id;
      const open = !!openIds[okey];
      const status = ap.total === 0 ? 'not' : allDone ? 'done' : ap.done > 0 ? 'prog' : 'not';
      const label = {
        done: 'Complete',
        prog: 'In Progress',
        not: 'Not Started'
      }[status];
      const meta = {
        done: {
          c: 'var(--success-ink)',
          bg: 'var(--success-bg)',
          bd: 'var(--success-border)'
        },
        prog: {
          c: 'var(--warning-ink)',
          bg: 'var(--warning-bg)',
          bd: 'var(--warning-border)'
        },
        not: {
          c: 'var(--neutral-ink)',
          bg: 'var(--neutral-bg)',
          bd: 'var(--neutral-border)'
        }
      }[status];
      return /*#__PURE__*/React.createElement("div", {
        key: co.id,
        style: {
          borderTop: '1px solid var(--line-3)'
        }
      }, /*#__PURE__*/React.createElement("div", {
        style: {
          display: 'grid',
          gridTemplateColumns: '26px 64px 1fr 96px 122px 28px',
          alignItems: 'center',
          gap: 10,
          padding: '10px 20px'
        }
      }, /*#__PURE__*/React.createElement("button", {
        onClick: () => setOpenIds(p => ({
          ...p,
          [okey]: !p[okey]
        })),
        style: {
          cursor: 'pointer',
          border: 'none',
          background: 'transparent',
          padding: 2,
          display: 'flex'
        }
      }, /*#__PURE__*/React.createElement(Icon, {
        name: "chevronRight",
        size: 14,
        strokeWidth: 2.4,
        color: "#B7B29A",
        style: {
          transform: `rotate(${open ? 90 : 0}deg)`,
          transition: 'transform 0.2s'
        }
      })), /*#__PURE__*/React.createElement("span", {
        style: {
          font: '700 10px var(--font-sans)',
          color: 'var(--gold-ink)'
        }
      }, co.code), /*#__PURE__*/React.createElement("button", {
        onClick: () => setOpenIds(p => ({
          ...p,
          [okey]: !p[okey]
        })),
        style: {
          font: '500 13px var(--font-sans)',
          color: '#33403a',
          background: 'transparent',
          border: 'none',
          textAlign: 'left',
          cursor: 'pointer',
          padding: 0
        }
      }, co.title), /*#__PURE__*/React.createElement("span", {
        style: {
          font: '500 11px var(--font-sans)',
          color: 'var(--text-faint-2)'
        }
      }, ap.done, "/", ap.total, " lessons"), /*#__PURE__*/React.createElement("span", {
        style: {
          justifySelf: 'start',
          font: '600 11px var(--font-sans)',
          padding: '5px 13px',
          borderRadius: 999,
          border: `1px solid ${meta.bd}`,
          color: meta.c,
          background: meta.bg
        }
      }, label), /*#__PURE__*/React.createElement(IconButton, {
        title: "Unassign course"
      })), /*#__PURE__*/React.createElement("div", {
        style: {
          display: 'grid',
          gridTemplateRows: open ? '1fr' : '0fr',
          transition: 'grid-template-rows 0.3s var(--ease-standard)'
        }
      }, /*#__PURE__*/React.createElement("div", {
        style: {
          overflow: 'hidden',
          minHeight: 0
        }
      }, /*#__PURE__*/React.createElement("div", {
        style: {
          padding: '2px 20px 14px 50px'
        }
      }, ap.lessons.map(l => {
        const done = !!db.lessonProgress[s.id + '|' + l.id];
        return /*#__PURE__*/React.createElement("div", {
          key: l.id,
          style: {
            padding: '11px 12px',
            borderRadius: 10,
            marginBottom: 7,
            border: `1px solid ${done ? '#C6DCC9' : '#EDE7D8'}`,
            background: done ? '#F1F7F2' : '#FDFCF8'
          }
        }, /*#__PURE__*/React.createElement("div", {
          style: {
            display: 'flex',
            alignItems: 'center',
            gap: 11
          }
        }, /*#__PURE__*/React.createElement("button", {
          onClick: () => onToggleProgress(s.id, l.id),
          style: {
            width: 22,
            height: 22,
            flex: 'none',
            borderRadius: 6,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            font: '700 12px var(--font-sans)',
            border: `1.5px solid ${done ? 'var(--primary-hex)' : '#C6BFA9'}`,
            background: done ? 'var(--primary-hex)' : '#fff',
            color: '#fff',
            cursor: 'pointer'
          }
        }, done ? '✓' : ''), /*#__PURE__*/React.createElement("span", {
          style: {
            flex: 1,
            minWidth: 0,
            font: '600 12.5px/1.3 var(--font-sans)',
            color: '#33403A'
          }
        }, l.title), l.est_min != null && /*#__PURE__*/React.createElement("span", {
          style: {
            flex: 'none',
            font: '600 9.5px var(--font-sans)',
            color: '#8A6A1E',
            background: '#F6ECD1',
            border: '1px solid #E7D5A2',
            padding: '2px 7px',
            borderRadius: 5
          }
        }, fmtMin(l.est_min))));
      })))));
    }), /*#__PURE__*/React.createElement("div", {
      style: {
        padding: '11px 20px',
        borderTop: '1px solid var(--line-3)',
        display: 'flex',
        gap: 10,
        flexWrap: 'wrap'
      }
    }, /*#__PURE__*/React.createElement(Button, {
      variant: "soft",
      size: "sm"
    }, "+ Assign course"), /*#__PURE__*/React.createElement(Button, {
      variant: "dashed",
      size: "sm"
    }, "+ Assign lesson"))));
  }))));
}
window.AssignmentsScreen = AssignmentsScreen;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/water-resources-lms/AssignmentsScreen.jsx", error: String((e && e.message) || e) }); }

// ui_kits/water-resources-lms/CurriculumScreen.jsx
try { (() => {
function CurriculumScreen({
  db,
  onEditCourseTitle,
  onEditLessonTitle,
  onToggleAvailable
}) {
  const ns = window.GHAUniversityWaterResourcesDesignSystem_a1ef01;
  const {
    Header,
    PageContent,
    SearchBar,
    NoResults,
    InlineEditText,
    LevelBadge,
    DisclosureCard,
    StatusPill,
    ResourceRow,
    Icon,
    Button
  } = ns;
  const {
    fmtMin,
    courseTime
  } = window.LmsHelpers;
  const [query, setQuery] = React.useState('');
  const [openCourses, setOpenCourses] = React.useState({
    c5: true
  });
  const q = query.toLowerCase().trim();
  const matchCourse = c => !q || c.code.toLowerCase().includes(q) || c.title.toLowerCase().includes(q) || c.lessons.some(l => l.title.toLowerCase().includes(q));
  const levelGroups = db.curriculumLevels.map(lv => ({
    lv,
    courses: db.courses.filter(c => c.level_id === lv.id && matchCourse(c))
  })).filter(x => x.courses.length > 0);
  const noResults = q.length > 0 && levelGroups.length === 0;
  return /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement(Header, {
    title: "Curriculum",
    toolbar: [{
      label: '+ Add course',
      primary: true
    }]
  }), /*#__PURE__*/React.createElement(PageContent, null, /*#__PURE__*/React.createElement(SearchBar, {
    value: query,
    onChange: setQuery,
    placeholder: "Search courses or lessons\u2026"
  }), noResults ? /*#__PURE__*/React.createElement(NoResults, {
    query: query
  }) : levelGroups.map(({
    lv,
    courses
  }) => /*#__PURE__*/React.createElement("div", {
    key: lv.id,
    style: {
      marginBottom: 30
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'baseline',
      gap: 12,
      marginBottom: 14
    }
  }, /*#__PURE__*/React.createElement(LevelBadge, null, lv.code, " LEVEL"), /*#__PURE__*/React.createElement("h2", {
    style: {
      font: '600 18px var(--font-serif)',
      color: 'var(--text-heading)'
    }
  }, lv.name)), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'grid',
      gridTemplateColumns: '1fr 1fr',
      gap: 12,
      alignItems: 'start'
    }
  }, courses.map(c => {
    const isOpen = !!openCourses[c.id];
    const resourceCount = c.lessons.reduce((a, l) => a + l.resources.length, 0);
    const tm = courseTime(c);
    return /*#__PURE__*/React.createElement(DisclosureCard, {
      key: c.id,
      open: isOpen,
      onToggle: () => setOpenCourses(p => ({
        ...p,
        [c.id]: !p[c.id]
      })),
      radius: 13,
      header: /*#__PURE__*/React.createElement("div", {
        style: {
          display: 'flex',
          gap: 12
        }
      }, /*#__PURE__*/React.createElement("span", {
        style: {
          font: '700 10px var(--font-sans)',
          letterSpacing: '0.03em',
          color: 'var(--gold-ink)',
          marginTop: 3
        }
      }, c.code), /*#__PURE__*/React.createElement("span", {
        style: {
          flex: 1,
          minWidth: 0
        }
      }, /*#__PURE__*/React.createElement(InlineEditText, {
        value: c.title,
        onCommit: v => onEditCourseTitle(c.id, v),
        style: {
          display: 'block',
          font: '600 15px/1.25 var(--font-serif)',
          color: '#2b332e'
        }
      }), /*#__PURE__*/React.createElement("span", {
        style: {
          display: 'block',
          font: '500 11px var(--font-sans)',
          color: 'var(--text-faint-2)',
          marginTop: 3
        }
      }, c.lessons.length, " lessons \xB7 ", resourceCount, " resources", tm ? ` · ~${fmtMin(tm)}` : '')))
    }, c.lessons.map((l, li) => {
      const avail = l.available !== false;
      return /*#__PURE__*/React.createElement("div", {
        key: l.id,
        style: {
          padding: '12px 0',
          borderBottom: '1px solid var(--line-3)'
        }
      }, /*#__PURE__*/React.createElement("div", {
        style: {
          display: 'flex',
          alignItems: 'center',
          gap: 10
        }
      }, /*#__PURE__*/React.createElement("span", {
        style: {
          flex: 'none',
          width: 22,
          height: 22,
          borderRadius: 6,
          background: 'var(--success-bg-strong)',
          color: 'var(--primary-hex)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          font: '700 11px var(--font-sans)'
        }
      }, li + 1), /*#__PURE__*/React.createElement(InlineEditText, {
        value: l.title,
        onCommit: v => onEditLessonTitle(l.id, v),
        style: {
          flex: 1,
          font: '600 13px/1.3 var(--font-sans)'
        }
      }), /*#__PURE__*/React.createElement(StatusPill, {
        status: avail ? 'available' : 'unavailable',
        onClick: () => onToggleAvailable(l.id)
      }), l.est_min != null && /*#__PURE__*/React.createElement("span", {
        style: {
          flex: 'none',
          display: 'inline-flex',
          alignItems: 'center',
          gap: 4,
          font: '600 10px var(--font-sans)',
          padding: '2px 7px',
          borderRadius: 6,
          color: '#8A6A1E',
          background: '#F6ECD1',
          border: '1px solid #E7D5A2'
        }
      }, /*#__PURE__*/React.createElement(Icon, {
        name: "clock",
        size: 10,
        strokeWidth: 2.2
      }), fmtMin(l.est_min))), l.resources.length > 0 && /*#__PURE__*/React.createElement("div", {
        style: {
          paddingLeft: 32,
          marginTop: 8
        }
      }, l.resources.map(r => /*#__PURE__*/React.createElement(ResourceRow, {
        key: r.id,
        type: r.type,
        title: r.title,
        meta: r.src,
        href: r.url
      }))));
    }), /*#__PURE__*/React.createElement("div", {
      style: {
        display: 'flex',
        gap: 10,
        marginTop: 12,
        flexWrap: 'wrap'
      }
    }, /*#__PURE__*/React.createElement(Button, {
      variant: "soft"
    }, "Assign course to\u2026"), /*#__PURE__*/React.createElement(Button, {
      variant: "dashed"
    }, "+ Add lesson")));
  }))))));
}
window.CurriculumScreen = CurriculumScreen;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/water-resources-lms/CurriculumScreen.jsx", error: String((e && e.message) || e) }); }

// ui_kits/water-resources-lms/DatabaseScreen.jsx
try { (() => {
function DatabaseScreen({
  db,
  onEditCourseTitle
}) {
  const ns = window.GHAUniversityWaterResourcesDesignSystem_a1ef01;
  const {
    Header,
    PageContent,
    SearchBar,
    Input,
    Select,
    CountBadge,
    IconButton,
    Button,
    Avatar,
    Icon
  } = ns;
  const [query, setQuery] = React.useState('');
  const [sectionOpen, setSectionOpen] = React.useState({
    courses: true,
    levels: false,
    staff: false,
    labor: false,
    skills: false
  });
  const [courseOpen, setCourseOpen] = React.useState({});
  function Section({
    label,
    count,
    k,
    children
  }) {
    const open = !!sectionOpen[k];
    return /*#__PURE__*/React.createElement("div", {
      style: {
        background: 'var(--surface)',
        border: '1px solid var(--border)',
        borderRadius: 14,
        boxShadow: 'var(--shadow-card)',
        overflow: 'hidden'
      }
    }, /*#__PURE__*/React.createElement("button", {
      onClick: () => setSectionOpen(p => ({
        ...p,
        [k]: !p[k]
      })),
      style: {
        display: 'flex',
        alignItems: 'center',
        gap: 10,
        width: '100%',
        cursor: 'pointer',
        border: 'none',
        background: 'var(--head-strip-bg)',
        padding: '14px 18px',
        font: '700 13.5px var(--font-serif)',
        color: 'var(--text-heading)'
      }
    }, /*#__PURE__*/React.createElement(Icon, {
      name: "chevronRight",
      size: 15,
      strokeWidth: 2.4,
      color: "#8A8570",
      style: {
        transform: `rotate(${open ? 90 : 0}deg)`,
        transition: 'transform 0.2s'
      }
    }), /*#__PURE__*/React.createElement("span", {
      style: {
        flex: 1,
        textAlign: 'left'
      }
    }, label), /*#__PURE__*/React.createElement(CountBadge, null, count)), /*#__PURE__*/React.createElement("div", {
      style: {
        display: 'grid',
        gridTemplateRows: open ? '1fr' : '0fr',
        transition: 'grid-template-rows 0.3s var(--ease-standard)'
      }
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        overflow: 'hidden',
        minHeight: 0
      }
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        padding: '12px 16px 16px',
        display: 'flex',
        flexDirection: 'column',
        gap: 8
      }
    }, children))));
  }
  return /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement(Header, {
    title: "Database",
    toolbar: [{
      label: '+ Add course',
      primary: true
    }]
  }), /*#__PURE__*/React.createElement(PageContent, null, /*#__PURE__*/React.createElement(SearchBar, {
    value: query,
    onChange: setQuery,
    placeholder: "Search courses or lessons\u2026"
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      flexDirection: 'column',
      gap: 14
    }
  }, /*#__PURE__*/React.createElement(Section, {
    label: "Courses & Lessons",
    count: db.courses.length,
    k: "courses"
  }, db.courses.map(c => {
    const cOpen = !!courseOpen[c.id];
    return /*#__PURE__*/React.createElement("div", {
      key: c.id,
      style: {
        border: '1px solid var(--line-3)',
        borderRadius: 10,
        overflow: 'hidden'
      }
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        display: 'grid',
        gridTemplateColumns: '96px 1fr 150px auto auto',
        gap: 8,
        alignItems: 'center',
        padding: '9px 11px',
        background: 'var(--head-strip-bg)'
      }
    }, /*#__PURE__*/React.createElement(Input, {
      value: c.code,
      readOnly: true
    }), /*#__PURE__*/React.createElement(Input, {
      value: c.title,
      onChange: e => onEditCourseTitle(c.id, e.target.value)
    }), /*#__PURE__*/React.createElement(Select, {
      value: c.level_id,
      readOnly: true
    }, db.curriculumLevels.map(l => /*#__PURE__*/React.createElement("option", {
      key: l.id,
      value: l.id
    }, l.code, " \xB7 ", l.name))), /*#__PURE__*/React.createElement("button", {
      onClick: () => setCourseOpen(p => ({
        ...p,
        [c.id]: !p[c.id]
      })),
      style: {
        cursor: 'pointer',
        border: '1px solid #dcd5c4',
        background: '#fff',
        color: '#6b6b5e',
        font: '600 11px var(--font-sans)',
        padding: '6px 10px',
        borderRadius: 7,
        display: 'flex',
        alignItems: 'center',
        gap: 6
      }
    }, /*#__PURE__*/React.createElement(Icon, {
      name: "chevronRight",
      size: 12,
      strokeWidth: 2.4,
      style: {
        transform: `rotate(${cOpen ? 90 : 0}deg)`,
        transition: 'transform 0.2s'
      }
    }), c.lessons.length, " lessons"), /*#__PURE__*/React.createElement(IconButton, {
      title: "Delete course"
    })), /*#__PURE__*/React.createElement("div", {
      style: {
        display: 'grid',
        gridTemplateRows: cOpen ? '1fr' : '0fr',
        transition: 'grid-template-rows 0.3s var(--ease-standard)'
      }
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        overflow: 'hidden',
        minHeight: 0
      }
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        padding: '8px 11px 11px',
        display: 'flex',
        flexDirection: 'column',
        gap: 6,
        borderTop: '1px solid var(--line)'
      }
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        display: 'grid',
        gridTemplateColumns: '1fr 96px 104px 28px',
        gap: 8,
        font: '600 9.5px var(--font-sans)',
        letterSpacing: '0.05em',
        textTransform: 'uppercase',
        color: 'var(--text-faint-2)',
        padding: '0 2px'
      }
    }, /*#__PURE__*/React.createElement("span", null, "Lesson"), /*#__PURE__*/React.createElement("span", null, "Est. (min)"), /*#__PURE__*/React.createElement("span", null, "Availability"), /*#__PURE__*/React.createElement("span", null)), c.lessons.map(l => /*#__PURE__*/React.createElement("div", {
      key: l.id,
      style: {
        display: 'grid',
        gridTemplateColumns: '1fr 96px 104px 28px',
        gap: 8,
        alignItems: 'center'
      }
    }, /*#__PURE__*/React.createElement(Input, {
      value: l.title,
      readOnly: true
    }), /*#__PURE__*/React.createElement(Input, {
      value: l.est_min ?? '',
      placeholder: "\u2014",
      readOnly: true
    }), /*#__PURE__*/React.createElement("span", {
      style: {
        cursor: 'pointer',
        font: '600 10px var(--font-sans)',
        padding: '6px 4px',
        borderRadius: 7,
        textAlign: 'center',
        border: `1px solid ${l.available !== false ? '#BBD8C4' : '#EAD1C7'}`,
        background: l.available !== false ? '#E1EEE6' : '#FBEDE8',
        color: l.available !== false ? 'var(--success-ink)' : 'var(--danger-ink)'
      }
    }, l.available !== false ? 'Available' : 'Unavailable'), /*#__PURE__*/React.createElement(IconButton, {
      title: "Delete lesson"
    })))))));
  }), /*#__PURE__*/React.createElement(Button, {
    variant: "soft"
  }, "+ Add course")), /*#__PURE__*/React.createElement(Section, {
    label: "Curriculum Levels",
    count: db.curriculumLevels.length,
    k: "levels"
  }, db.curriculumLevels.map(l => /*#__PURE__*/React.createElement("div", {
    key: l.id,
    style: {
      display: 'grid',
      gridTemplateColumns: '96px 1fr 92px 28px',
      gap: 8,
      alignItems: 'center'
    }
  }, /*#__PURE__*/React.createElement(Input, {
    value: l.code,
    readOnly: true
  }), /*#__PURE__*/React.createElement(Input, {
    value: l.name,
    readOnly: true
  }), /*#__PURE__*/React.createElement("span", {
    style: {
      font: '500 11px var(--font-sans)',
      color: 'var(--text-faint-2)'
    }
  }, db.courses.filter(c => c.level_id === l.id).length, " courses"), /*#__PURE__*/React.createElement(IconButton, {
    title: "Delete level"
  }))), /*#__PURE__*/React.createElement(Button, {
    variant: "dashed"
  }, "+ Add level")), /*#__PURE__*/React.createElement(Section, {
    label: "Staff",
    count: db.staff.length,
    k: "staff"
  }, db.staff.map(s => /*#__PURE__*/React.createElement("div", {
    key: s.id,
    style: {
      display: 'grid',
      gridTemplateColumns: '32px 1fr 130px 28px',
      gap: 8,
      alignItems: 'center'
    }
  }, /*#__PURE__*/React.createElement(Avatar, {
    name: s.name,
    size: 30
  }), /*#__PURE__*/React.createElement(Input, {
    value: s.name,
    readOnly: true
  }), /*#__PURE__*/React.createElement(Select, {
    value: s.labor_cat_id ?? '',
    readOnly: true
  }, db.laborCategories.map(c => /*#__PURE__*/React.createElement("option", {
    key: c.id,
    value: c.id
  }, c.code))), /*#__PURE__*/React.createElement(IconButton, {
    title: "Remove staff member"
  }))), /*#__PURE__*/React.createElement(Button, {
    variant: "soft"
  }, "+ Add staff")), /*#__PURE__*/React.createElement(Section, {
    label: "Labor Categories",
    count: db.laborCategories.length,
    k: "labor"
  }, db.laborCategories.map(c => /*#__PURE__*/React.createElement("div", {
    key: c.id,
    style: {
      display: 'grid',
      gridTemplateColumns: '1fr 28px',
      gap: 8,
      alignItems: 'center'
    }
  }, /*#__PURE__*/React.createElement(Input, {
    value: c.code,
    readOnly: true
  }), /*#__PURE__*/React.createElement(IconButton, {
    title: "Delete labor category"
  }))), /*#__PURE__*/React.createElement(Button, {
    variant: "dashed"
  }, "+ Add category")), /*#__PURE__*/React.createElement(Section, {
    label: "Skill Groups",
    count: db.skillGroups.reduce((a, g) => a + g.skills.length, 0),
    k: "skills"
  }, db.skillGroups.map(g => /*#__PURE__*/React.createElement("div", {
    key: g.id,
    style: {
      border: '1px solid var(--line-3)',
      borderRadius: 10,
      padding: '9px 11px',
      display: 'flex',
      flexDirection: 'column',
      gap: 6
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'grid',
      gridTemplateColumns: '1fr 28px',
      gap: 8,
      alignItems: 'center'
    }
  }, /*#__PURE__*/React.createElement(Input, {
    value: g.name,
    readOnly: true,
    style: {
      fontWeight: 600
    }
  }), /*#__PURE__*/React.createElement(IconButton, {
    title: "Delete skill group"
  })), g.skills.map(sk => /*#__PURE__*/React.createElement("div", {
    key: sk.id,
    style: {
      display: 'grid',
      gridTemplateColumns: '1fr 28px',
      gap: 8,
      alignItems: 'center',
      paddingLeft: 10
    }
  }, /*#__PURE__*/React.createElement(Input, {
    value: sk.name,
    readOnly: true
  }), /*#__PURE__*/React.createElement(IconButton, {
    title: "Delete skill"
  }))))), /*#__PURE__*/React.createElement(Button, {
    variant: "soft"
  }, "+ Add skill group")))));
}
window.DatabaseScreen = DatabaseScreen;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/water-resources-lms/DatabaseScreen.jsx", error: String((e && e.message) || e) }); }

// ui_kits/water-resources-lms/LoginScreen.jsx
try { (() => {
function LoginScreen({
  onSignIn
}) {
  const {
    Logo
  } = window.GHAUniversityWaterResourcesDesignSystem_a1ef01;
  const [email, setEmail] = React.useState('');
  const [password, setPassword] = React.useState('');
  const [error, setError] = React.useState('');
  function submit(e) {
    e.preventDefault();
    if (!email || !password) {
      setError('Enter your email and password.');
      return;
    }
    setError('');
    onSignIn(email);
  }
  return /*#__PURE__*/React.createElement("div", {
    style: {
      minHeight: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '40px 20px'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      width: '100%',
      maxWidth: 404,
      background: 'var(--surface)',
      border: '1px solid var(--border)',
      borderRadius: 20,
      boxShadow: 'var(--shadow-card)',
      padding: '38px 36px 28px',
      animation: 'cardIn 0.5s var(--ease-entrance) both'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 12,
      marginBottom: 26
    }
  }, /*#__PURE__*/React.createElement(Logo, {
    size: 38
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      lineHeight: 1.1
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      font: '800 15px var(--font-sans)',
      color: 'var(--text-heading)',
      letterSpacing: '0.01em'
    }
  }, "GHA University"), /*#__PURE__*/React.createElement("div", {
    style: {
      font: '600 9px var(--font-sans)',
      letterSpacing: '0.15em',
      textTransform: 'uppercase',
      color: '#7ba98c',
      marginTop: 2
    }
  }, "Water Resources"))), /*#__PURE__*/React.createElement("h1", {
    style: {
      font: '600 25px/1.15 var(--font-serif)',
      color: 'var(--text-heading)',
      margin: '0 0 24px'
    }
  }, "Sign in"), /*#__PURE__*/React.createElement("form", {
    onSubmit: submit,
    style: {
      display: 'flex',
      flexDirection: 'column',
      gap: 15
    }
  }, /*#__PURE__*/React.createElement("label", null, /*#__PURE__*/React.createElement("span", {
    style: {
      display: 'block',
      font: '600 11px var(--font-sans)',
      color: 'var(--text-muted)',
      marginBottom: 6
    }
  }, "Email"), /*#__PURE__*/React.createElement("input", {
    type: "email",
    value: email,
    onChange: e => {
      setEmail(e.target.value);
      setError('');
    },
    placeholder: "you@gha-engineers.com",
    autoComplete: "username",
    style: {
      width: '100%',
      padding: '11px 13px',
      border: '1px solid var(--line-input)',
      borderRadius: 10,
      font: '500 13.5px var(--font-sans)',
      color: 'var(--text-body)',
      background: '#fff'
    }
  })), /*#__PURE__*/React.createElement("label", null, /*#__PURE__*/React.createElement("span", {
    style: {
      display: 'block',
      font: '600 11px var(--font-sans)',
      color: 'var(--text-muted)',
      marginBottom: 6
    }
  }, "Password"), /*#__PURE__*/React.createElement("input", {
    type: "password",
    value: password,
    onChange: e => {
      setPassword(e.target.value);
      setError('');
    },
    placeholder: "\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022",
    autoComplete: "current-password",
    style: {
      width: '100%',
      padding: '11px 13px',
      border: '1px solid var(--line-input)',
      borderRadius: 10,
      font: '500 13.5px var(--font-sans)',
      color: 'var(--text-body)',
      background: '#fff'
    }
  })), error && /*#__PURE__*/React.createElement("div", {
    style: {
      font: '500 12px/1.45 var(--font-sans)',
      color: 'var(--danger-ink)',
      background: 'var(--danger-bg)',
      border: '1px solid var(--danger-border)',
      padding: '9px 12px',
      borderRadius: 9
    }
  }, error), /*#__PURE__*/React.createElement("button", {
    type: "submit",
    style: {
      cursor: 'pointer',
      border: 'none',
      background: 'var(--primary-hex)',
      color: '#fff',
      font: '700 13.5px var(--font-sans)',
      padding: '12px 18px',
      borderRadius: 11,
      marginTop: 4
    }
  }, "Sign in"))));
}
window.LoginScreen = LoginScreen;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/water-resources-lms/LoginScreen.jsx", error: String((e && e.message) || e) }); }

// ui_kits/water-resources-lms/MatrixScreen.jsx
try { (() => {
function MatrixScreen({
  db,
  onToggleProgress
}) {
  const ns = window.GHAUniversityWaterResourcesDesignSystem_a1ef01;
  const {
    Header,
    PageContent,
    SearchBar,
    NoResults,
    Surface,
    Avatar,
    MatrixCell,
    LessonToggleCell,
    Icon
  } = ns;
  const {
    fmtMin,
    lcCode
  } = window.LmsHelpers;
  const [query, setQuery] = React.useState('');
  const [openIds, setOpenIds] = React.useState({});
  const q = query.toLowerCase().trim();
  const staff = db.staff;
  const matchCourse = c => !q || c.code.toLowerCase().includes(q) || c.title.toLowerCase().includes(q) || c.lessons.some(l => l.title.toLowerCase().includes(q));
  const levelGroups = db.curriculumLevels.map(lv => ({
    lv,
    courses: db.courses.filter(c => c.level_id === lv.id && matchCourse(c))
  })).filter(x => x.courses.length > 0);
  const noResults = q.length > 0 && levelGroups.length === 0;
  const gridTemplateColumns = `minmax(240px,1.6fr) repeat(${staff.length}, minmax(84px,1fr))`;
  const minWidth = 260 + staff.length * 90;
  const rowStyle = {
    gridTemplateColumns,
    minWidth,
    display: 'grid'
  };
  const LEGEND = [{
    label: 'Not started',
    style: {
      background: '#F6F3EC',
      border: '1px solid #ECE6D8'
    }
  }, {
    label: 'In progress',
    style: {
      background: 'var(--warning-swatch)'
    }
  }, {
    label: 'Complete',
    style: {
      background: 'var(--primary-hex)'
    }
  }, {
    label: 'Unavailable lesson',
    style: {
      background: '#F7F0EB',
      border: '1.5px solid #E4D6CB'
    }
  }];
  return /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement(Header, {
    title: "Training Matrix",
    toolbar: []
  }), /*#__PURE__*/React.createElement(PageContent, null, /*#__PURE__*/React.createElement(SearchBar, {
    value: query,
    onChange: setQuery,
    placeholder: "Search courses or lessons\u2026"
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      flexWrap: 'wrap',
      gap: 16,
      marginBottom: 6
    }
  }, LEGEND.map(lg => /*#__PURE__*/React.createElement("div", {
    key: lg.label,
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 8,
      font: '500 12px var(--font-sans)',
      color: '#6b6b5e'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      width: 16,
      height: 16,
      borderRadius: 5,
      display: 'inline-block',
      ...lg.style
    }
  }), lg.label)), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 8,
      font: '500 12px var(--font-sans)',
      color: '#6b6b5e'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      width: 16,
      height: 16,
      borderRadius: 5,
      background: 'var(--primary-hex)',
      color: '#fff',
      display: 'inline-flex',
      alignItems: 'center',
      justifyContent: 'center',
      fontSize: 10,
      fontWeight: 700
    }
  }, "\u2713"), "Lesson done")), /*#__PURE__*/React.createElement("div", {
    style: {
      font: '500 11.5px var(--font-sans)',
      color: 'var(--text-faint-2)',
      marginBottom: 12
    }
  }, "Expand a course to tick individual lessons \u2014 course cells are read-only and populate automatically from lesson status."), noResults ? /*#__PURE__*/React.createElement(NoResults, {
    query: query
  }) : /*#__PURE__*/React.createElement(Surface, {
    style: {
      overflow: 'auto',
      borderRadius: 16
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      ...rowStyle,
      borderBottom: '1px solid var(--line-2)'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      padding: '12px 16px',
      font: '600 11px var(--font-sans)',
      letterSpacing: '0.04em',
      textTransform: 'uppercase',
      color: 'var(--text-faint)',
      background: 'var(--head-strip-bg)',
      position: 'sticky',
      left: 0
    }
  }, "Course"), staff.map(s => /*#__PURE__*/React.createElement("div", {
    key: s.id,
    style: {
      padding: '10px 6px',
      textAlign: 'center',
      background: 'var(--head-strip-bg)',
      borderLeft: '1px solid var(--line)'
    }
  }, /*#__PURE__*/React.createElement(Avatar, {
    name: s.name,
    size: 28
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      font: '600 10.5px var(--font-sans)',
      color: '#33403a',
      whiteSpace: 'nowrap',
      marginTop: 4
    }
  }, s.name.split(' ')[0]), /*#__PURE__*/React.createElement("div", {
    style: {
      font: '500 9px var(--font-sans)',
      color: 'var(--text-faint-2)'
    }
  }, lcCode(db, s))))), levelGroups.map(({
    lv,
    courses
  }) => /*#__PURE__*/React.createElement(React.Fragment, {
    key: lv.id
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      ...rowStyle,
      gridColumn: '1 / -1',
      padding: '9px 16px',
      font: '700 10.5px var(--font-sans)',
      letterSpacing: '0.06em',
      textTransform: 'uppercase',
      color: 'var(--primary-hex)',
      background: '#eef4ef',
      borderTop: '1px solid #e1eae2',
      borderBottom: '1px solid #e1eae2'
    }
  }, lv.code, " \xB7 ", lv.name), courses.map(c => {
    const open = !!openIds[c.id];
    return /*#__PURE__*/React.createElement(React.Fragment, {
      key: c.id
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        ...rowStyle,
        borderTop: '1px solid var(--line-4)'
      }
    }, /*#__PURE__*/React.createElement("button", {
      onClick: () => setOpenIds(p => ({
        ...p,
        [c.id]: !p[c.id]
      })),
      style: {
        padding: '10px 16px',
        font: '500 12.5px/1.3 var(--font-sans)',
        color: '#33403a',
        display: 'flex',
        alignItems: 'center',
        gap: 8,
        background: '#fff',
        position: 'sticky',
        left: 0,
        border: 'none',
        cursor: 'pointer',
        textAlign: 'left'
      }
    }, /*#__PURE__*/React.createElement(Icon, {
      name: "chevronRight",
      size: 14,
      strokeWidth: 2.4,
      color: "#B7B29A",
      style: {
        transform: `rotate(${open ? 90 : 0}deg)`,
        transition: 'transform 0.2s'
      }
    }), /*#__PURE__*/React.createElement("span", {
      style: {
        font: '700 9.5px var(--font-sans)',
        color: 'var(--gold-ink-2)'
      }
    }, c.code), c.title), staff.map(s => {
      const total = c.lessons.length;
      const done = c.lessons.filter(l => !!db.lessonProgress[s.id + '|' + l.id]).length;
      const state = total === 0 || done === 0 ? 'empty' : done === total ? 'done' : 'prog';
      return /*#__PURE__*/React.createElement("div", {
        key: s.id,
        style: {
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          padding: '8px 6px',
          borderLeft: '1px solid var(--line-4)'
        }
      }, /*#__PURE__*/React.createElement(MatrixCell, {
        state: state,
        label: state === 'prog' ? `${done}/${total}` : '',
        title: `${s.name} — ${c.code}`
      }));
    })), open && c.lessons.map((l, li) => {
      const avail = l.available !== false;
      return /*#__PURE__*/React.createElement("div", {
        key: l.id,
        style: {
          ...rowStyle,
          animation: 'rowIn 0.28s ease both'
        }
      }, /*#__PURE__*/React.createElement("div", {
        style: {
          padding: '6px 16px 6px 34px',
          font: '500 11.5px/1.25 var(--font-sans)',
          color: '#5c6660',
          display: 'flex',
          alignItems: 'center',
          gap: 8,
          background: 'var(--head-strip-bg)',
          position: 'sticky',
          left: 0
        }
      }, /*#__PURE__*/React.createElement("span", {
        style: {
          color: 'var(--gold-ink-2)',
          font: '700 9.5px var(--font-sans)'
        }
      }, li + 1), /*#__PURE__*/React.createElement("span", {
        style: {
          flex: 1,
          minWidth: 0
        }
      }, l.title), !avail && /*#__PURE__*/React.createElement("span", {
        style: {
          font: '700 8px var(--font-sans)',
          letterSpacing: '0.04em',
          textTransform: 'uppercase',
          color: 'var(--danger-ink)',
          background: 'var(--danger-bg)',
          border: '1px solid var(--danger-border)',
          padding: '1px 6px',
          borderRadius: 5
        }
      }, "Unavail")), staff.map(s => /*#__PURE__*/React.createElement("div", {
        key: s.id,
        style: {
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          padding: '5px 6px',
          borderLeft: '1px solid var(--line-4)',
          background: 'var(--head-strip-bg)'
        }
      }, /*#__PURE__*/React.createElement(LessonToggleCell, {
        done: !!db.lessonProgress[s.id + '|' + l.id],
        available: avail,
        onClick: () => onToggleProgress(s.id, l.id),
        title: `${s.name} — ${l.title}`
      }))));
    }));
  }))))));
}
window.MatrixScreen = MatrixScreen;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/water-resources-lms/MatrixScreen.jsx", error: String((e && e.message) || e) }); }

// ui_kits/water-resources-lms/SkillsScreen.jsx
try { (() => {
function SkillsScreen({
  db,
  onCycleRating
}) {
  const ns = window.GHAUniversityWaterResourcesDesignSystem_a1ef01;
  const {
    Header,
    PageContent,
    Surface,
    Avatar,
    ProficiencyChip,
    IconButton,
    Button
  } = ns;
  const {
    lcCode
  } = window.LmsHelpers;
  const staff = db.staff;
  const gridTemplateColumns = `minmax(230px,1.5fr) repeat(${staff.length}, minmax(96px,1fr))`;
  const minWidth = 250 + staff.length * 104;
  const rowStyle = {
    gridTemplateColumns,
    minWidth,
    display: 'grid'
  };
  const LEGEND = [{
    label: 'None',
    bg: 'var(--prof-none-bg)',
    bd: 'var(--prof-none-border)',
    tc: 'var(--prof-none-ink)'
  }, {
    label: 'Learning',
    bg: 'var(--prof-learning-bg)',
    bd: 'var(--prof-learning-border)',
    tc: 'var(--prof-learning-ink)'
  }, {
    label: 'Proficient',
    bg: 'var(--prof-proficient-bg)',
    bd: 'var(--prof-proficient-border)',
    tc: 'var(--prof-proficient-ink)'
  }, {
    label: 'Expert',
    bg: 'var(--prof-expert-bg)',
    bd: 'var(--prof-expert-border)',
    tc: 'var(--prof-expert-ink)'
  }];
  return /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement(Header, {
    title: "Skills & Experience",
    toolbar: [{
      label: '+ Add staff',
      primary: true
    }]
  }), /*#__PURE__*/React.createElement(PageContent, null, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      flexWrap: 'wrap',
      alignItems: 'center',
      gap: 14,
      marginBottom: 16
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      font: '500 12px var(--font-sans)',
      color: '#6b6b5e'
    }
  }, "Click a cell to cycle proficiency:"), LEGEND.map(p => /*#__PURE__*/React.createElement("span", {
    key: p.label,
    style: {
      font: '600 11px var(--font-sans)',
      padding: '3px 12px',
      borderRadius: 7,
      border: `1px solid ${p.bd}`,
      background: p.bg,
      color: p.tc
    }
  }, p.label))), /*#__PURE__*/React.createElement(Surface, {
    style: {
      overflow: 'auto',
      borderRadius: 16
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      ...rowStyle,
      position: 'sticky',
      top: 0,
      zIndex: 2
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      padding: '12px 16px',
      font: '600 11px var(--font-sans)',
      letterSpacing: '0.04em',
      textTransform: 'uppercase',
      color: '#eaf2eb',
      background: 'var(--primary-hex)',
      position: 'sticky',
      left: 0
    }
  }, "Skill / Capability"), staff.map(s => /*#__PURE__*/React.createElement("div", {
    key: s.id,
    style: {
      padding: '9px 6px',
      textAlign: 'center',
      background: 'var(--primary-hex)',
      borderLeft: '1px solid rgba(255,255,255,0.1)'
    }
  }, /*#__PURE__*/React.createElement(Avatar, {
    name: s.name,
    size: 26
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      font: '600 10.5px var(--font-sans)',
      color: '#eaf2eb',
      whiteSpace: 'nowrap',
      marginTop: 4
    }
  }, s.name.split(' ')[0]), /*#__PURE__*/React.createElement("div", {
    style: {
      font: '500 9px var(--font-sans)',
      color: '#b9d8c3'
    }
  }, lcCode(db, s))))), db.skillGroups.map(g => /*#__PURE__*/React.createElement(React.Fragment, {
    key: g.id
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      ...rowStyle,
      gridColumn: '1 / -1',
      alignItems: 'center',
      gap: 10,
      padding: '8px 16px',
      font: '700 10.5px var(--font-sans)',
      letterSpacing: '0.06em',
      textTransform: 'uppercase',
      color: 'var(--primary-hex)',
      background: '#eef4ef',
      borderTop: '1px solid #e1eae2',
      borderBottom: '1px solid #e1eae2'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      flex: 1
    }
  }, g.name), /*#__PURE__*/React.createElement(Button, {
    variant: "secondary",
    size: "sm"
  }, "+ Skill")), g.skills.map(sk => /*#__PURE__*/React.createElement("div", {
    key: sk.id,
    style: {
      ...rowStyle,
      borderTop: '1px solid var(--line-4)'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      padding: '7px 16px',
      font: '500 12px/1.25 var(--font-sans)',
      color: '#33403a',
      display: 'flex',
      alignItems: 'center',
      gap: 8,
      background: '#fff',
      position: 'sticky',
      left: 0
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      flex: 1
    }
  }, sk.name), /*#__PURE__*/React.createElement(IconButton, {
    title: "Delete skill",
    size: 12
  })), staff.map(s => {
    const v = db.skillRatings[s.id + '|' + sk.id] ?? 0;
    return /*#__PURE__*/React.createElement("div", {
      key: s.id,
      style: {
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '6px 8px',
        borderLeft: '1px solid var(--line-4)'
      }
    }, /*#__PURE__*/React.createElement(ProficiencyChip, {
      level: v,
      onClick: () => onCycleRating(s.id, sk.id)
    }));
  }))))))));
}
window.SkillsScreen = SkillsScreen;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/water-resources-lms/SkillsScreen.jsx", error: String((e && e.message) || e) }); }

// ui_kits/water-resources-lms/data.js
try { (() => {
/* Sample data for the GHA University UI kit — abbreviated but verbatim from
   supabase/seed.sql (real course/lesson/resource titles, real staff names,
   real labor categories and skill names). Attached to window so every
   screen script (each its own Babel scope) can read it. */
(function () {
  const laborCategories = [{
    id: 'lc-intern',
    code: 'INTERN'
  }, {
    id: 'lc-1',
    code: 'ENG I'
  }, {
    id: 'lc-2',
    code: 'ENG II'
  }, {
    id: 'lc-3',
    code: 'ENG III'
  }, {
    id: 'lc-4',
    code: 'ENG IV'
  }];
  const staff = [{
    id: 's1',
    name: 'Nicole Alvarez',
    labor_cat_id: 'lc-1'
  }, {
    id: 's2',
    name: 'Logan Reyes',
    labor_cat_id: 'lc-1'
  }, {
    id: 's3',
    name: 'Iza Kovács',
    labor_cat_id: 'lc-2'
  }, {
    id: 's4',
    name: 'Cesar Ramos',
    labor_cat_id: 'lc-3'
  }, {
    id: 's5',
    name: 'Monica Doyle',
    labor_cat_id: 'lc-4'
  }, {
    id: 's6',
    name: 'Bella Nguyen',
    labor_cat_id: 'lc-intern'
  }];
  const curriculumLevels = [{
    id: 'lv-000',
    code: '000',
    name: 'ONBOARDING'
  }, {
    id: 'lv-100',
    code: '100',
    name: 'FUNDAMENTALS'
  }, {
    id: 'lv-200',
    code: '200',
    name: 'DESIGN'
  }, {
    id: 'lv-300',
    code: '300',
    name: 'ADVANCED TOPICS'
  }, {
    id: 'lv-400',
    code: '400',
    name: 'PROJECT MANAGEMENT'
  }];
  let uid = 1;
  const nid = p => p + uid++;
  function lesson(title, est_min, available, resources) {
    return {
      id: nid('l'),
      title,
      est_min: est_min ?? null,
      available: available !== false,
      resources: resources || []
    };
  }
  function res(type, title, src, url) {
    return {
      id: nid('r'),
      type,
      title,
      src: src || null,
      url: url || null
    };
  }
  const courses = [{
    id: 'c1',
    code: 'WR-001',
    level_id: 'lv-000',
    title: "Division Overview & Culture",
    lessons: [lesson("Division's purpose, services, & clients", null, false), lesson('How the division contributes to the GHA mission', null, false), lesson('Culture expectations — ownership, communication, responsiveness', null, false)]
  }, {
    id: 'c2',
    code: 'WR-003',
    level_id: 'lv-000',
    title: 'Systems, Tools, & Technology',
    lessons: [lesson('Software installation', null, false), lesson('SmartSheet', null, false), lesson('File structure & naming conventions', null, true, [res('doc', 'Folder Structure Outline 2026.docx + 2026 Folder Structure Transition.xlsx', 'P:\\Water Resources\\Admin\\_Folder Structure')])]
  }, {
    id: 'c3',
    code: 'WR-103',
    level_id: 'lv-100',
    title: 'Floodplain Basics',
    lessons: [lesson('Floodway, flood fringe & BFE', 30, true, [res('doc', 'CFM Exam Resources — Floodplain Mapping (sample FIRMs/FIS)', 'P:\\Water Resources\\Staff Development\\Licensing\\CFM')]), lesson('Compensatory storage', 45, true, [res('doc', 'Floodplain Compensatory Storage Calculations.xlsx', 'P:\\Water Resources\\Stormwater\\Calculations')]), lesson('CLOMR / LOMR / LOMR-F', 40, true, [res('doc', 'Revising Your Maps — Insight on the LOMR/CLOMR Process', 'P:\\Water Resources\\Staff Development\\Training\\External'), res('doc', 'IDNR-OWR Floodplain Map Revision Manual (2025 beta)', 'P:\\Water Resources\\Stormwater\\Permitting\\FEMA Map Revisions')]), lesson('Depressional vs. riverine floodplain', null, false)]
  }, {
    id: 'c4',
    code: 'WR-105',
    level_id: 'lv-100',
    title: 'GIS Basics',
    lessons: [lesson('Create a project', null, false), lesson('Symbolize your data', null, false), lesson('Use geoprocessing tools', null, false)]
  }, {
    id: 'c5',
    code: 'WR-201',
    level_id: 'lv-200',
    title: 'Detention Design',
    lessons: [lesson('Detention routing in PondPack', 60, true, [res('doc', 'PondPack Template (.ppc/.dwh/.mdb)', 'P:\\Water Resources\\Stormwater\\Modeling\\PondPack\\Template')]), lesson('Detention routing in Excel — Modified Rational Method with Bulletin 75', 50, true, [res('doc', 'DetentionVolume_ModRational_Bul75.xlsx', 'P:\\Water Resources\\Stormwater\\Calculations\\Formatted_Spreadsheets'), res('doc', 'Stage Storage Calculation.xlsx', 'P:\\Water Resources\\Stormwater\\Calculations\\_New Formatted Spreadsheets')]), lesson('Graded surface storage basins', 35, true, [res('doc', 'Grading Examples (9 files)', 'P:\\Water Resources\\Stormwater\\Design References\\Grading Examples')]), lesson('Underground storage', 40, true, [res('doc', 'StormTrap Hydrodynamic Separator specs (22 files)', 'P:\\Water Resources\\Stormwater\\Design References\\Products\\StormTrap')]), lesson('Outlet control structures & overflow weirs', 30, true, [res('doc', 'OutletControl.xlsx', 'P:\\Water Resources\\Stormwater\\Calculations\\Formatted_Spreadsheets')]), lesson('Naturalized vs. turf grass basins', null, true, [res('doc', 'Wetland Naturalized Basin w/ Emergent Channel — Miller Park example', 'P:\\Water Resources\\Stormwater\\Design References\\BMPs')])]
  }, {
    id: 'c6',
    code: 'WR-203',
    level_id: 'lv-200',
    title: 'Storm Sewer Design',
    lessons: [lesson('Excel storm sewer sizing & HGL', 55, true, [res('doc', 'Storm Sewer Design - HGL - Bulletin 75_Huff.xlsx', 'P:\\Water Resources\\Stormwater\\Calculations')]), lesson('Runoff coefficients & time of concentration', 40, true, [res('doc', 'Runoff Coefficients.xlsx', 'P:\\Water Resources\\Stormwater\\Calculations\\Storm Sewer')]), lesson('Pipe capacity, cover & sizing', 35, true, [res('doc', 'Storm Sewer Cover Calculator.xlsx', 'P:\\Water Resources\\Stormwater\\Calculations\\Storm Sewer')]), lesson('Inlet & grate capacity, spacing', 35, true, [res('doc', 'Master_Inlet Spacing (template + project examples)', 'P:\\Water Resources\\Stormwater\\Calculations\\Inlet Spacing & Capacity')]), lesson('100-yr overland flow paths', null, false)]
  }, {
    id: 'c7',
    code: 'WR-303',
    level_id: 'lv-300',
    title: 'HEC-RAS',
    lessons: [lesson('1D steady/unsteady flow fundamentals', 90, true, [res('doc', '2025 ASCE EWRI HEC-RAS Beginner Course — full notebook & manuals', 'P:\\Water Resources\\Staff Development\\Training\\External')]), lesson('Bridge modeling', 60, true, [res('doc', '2024 IAFSM 2D HEC-RAS Training — Workshop 2 (2D Bridge Modeling)', 'P:\\Water Resources\\Staff Development\\Training\\External')]), lesson('2D modeling', 60, true, [res('doc', '2024 IAFSM 2D HEC-RAS Training — Workshop 3-5, L08-L09', 'P:\\Water Resources\\Staff Development\\Training\\External')])]
  }, {
    id: 'c8',
    code: 'WR-314',
    level_id: 'lv-300',
    title: 'Stormwater Grant Applications',
    lessons: [lesson('Matching projects to programs (local cost-share vs. federal competitive)', 25, true, [res('link', "Lake County 'Stormwater Grants in Action' book", 'P:\\Water Resources\\Grants\\Lake County SMC\\DCEO', 'https://mwrd.org/stormwater/partnerships')]), lesson('Estimating Design Retention Capacity (DRC) for GI applications', 30, true, [res('doc', 'DRC Calc_r2026-01 ($pergal).xlsx', 'P:\\Water Resources\\Grants\\MWRD\\GIPP\\Norridge GI')]), lesson('Assembling a competitive federal application', null, false)]
  }, {
    id: 'c9',
    code: 'WR-401',
    level_id: 'lv-400',
    title: 'Proposals',
    lessons: [lesson('Scope & fee proposals', 30, true, [res('doc', 'Proposal Scope Templates — Stormwater (10 files) & Wetlands (4 files)', 'P:\\Water Resources\\Templates\\Proposal Scope Templates')]), lesson('SOIs (Statements of Interest)', null, false), lesson('Subconsultants', 20, true, [res('doc', 'GHA Subconsultant Master Services Agreement & Work Order templates', 'P:\\Water Resources\\Admin\\Subconsultants')])]
  }];
  const skillGroups = [{
    id: 'sg1',
    name: 'H&H Software',
    skills: [{
      id: 'sk1',
      name: 'Bentley PondPack'
    }, {
      id: 'sk2',
      name: 'HEC-RAS'
    }, {
      id: 'sk3',
      name: 'HEC-HMS'
    }, {
      id: 'sk4',
      name: 'XPSWMM'
    }, {
      id: 'sk5',
      name: 'Hydraflow'
    }, {
      id: 'sk6',
      name: 'HY-8'
    }]
  }, {
    id: 'sg2',
    name: 'Stormwater Tasks',
    skills: [{
      id: 'sk7',
      name: 'Storm Sewer Design (Spreadsheet)'
    }, {
      id: 'sk8',
      name: 'Detention Design'
    }, {
      id: 'sk9',
      name: 'Inlet Spacing / Inlet Capacity'
    }, {
      id: 'sk10',
      name: 'Overflow Route Analysis'
    }]
  }];

  // Seed a handful of assignments/progress/ratings so the Assignments/Matrix/Skills
  // screens don't render fully empty on first paint.
  const lessonAssign = {};
  const lessonProgress = {};
  const skillRatings = {};
  function assign(staffId, lessonId, done) {
    lessonAssign[staffId + '|' + lessonId] = true;
    if (done) lessonProgress[staffId + '|' + lessonId] = true;
  }
  const c5 = courses.find(c => c.id === 'c5');
  const c6 = courses.find(c => c.id === 'c6');
  const c3 = courses.find(c => c.id === 'c3');
  assign('s1', c5.lessons[0].id, true);
  assign('s1', c5.lessons[1].id, true);
  assign('s1', c5.lessons[2].id, false);
  assign('s1', c6.lessons[0].id, true);
  assign('s2', c3.lessons[0].id, true);
  assign('s2', c3.lessons[1].id, false);
  assign('s3', c5.lessons[0].id, true);
  assign('s3', c5.lessons[1].id, true);
  assign('s3', c5.lessons[2].id, true);
  assign('s3', c5.lessons[3].id, true);
  assign('s4', c6.lessons[0].id, true);
  assign('s4', c6.lessons[1].id, true);
  skillRatings['s1|sk2'] = 1;
  skillRatings['s1|sk1'] = 2;
  skillRatings['s3|sk2'] = 3;
  skillRatings['s3|sk1'] = 3;
  skillRatings['s3|sk8'] = 2;
  skillRatings['s4|sk8'] = 3;
  skillRatings['s4|sk9'] = 2;
  skillRatings['s5|sk2'] = 3;
  skillRatings['s5|sk3'] = 3;
  skillRatings['s5|sk8'] = 3;
  window.SEED_DATA = {
    laborCategories,
    staff,
    curriculumLevels,
    courses,
    skillGroups,
    lessonAssign,
    lessonProgress,
    skillRatings
  };
})();
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/water-resources-lms/data.js", error: String((e && e.message) || e) }); }

// ui_kits/water-resources-lms/helpers.js
try { (() => {
(function () {
  function fmtMin(m) {
    if (m == null || isNaN(m)) return '';
    const n = Math.trunc(m);
    if (n >= 60) {
      const h = Math.floor(n / 60);
      const mm = n % 60;
      return h + 'h' + (mm ? ' ' + mm + 'm' : '');
    }
    return n + ' min';
  }
  function courseTime(course) {
    return course.lessons.reduce((a, l) => a + (l.est_min || 0), 0);
  }
  function initials(name) {
    return (name || '').trim().split(/\s+/).map(w => w[0] || '').slice(0, 2).join('').toUpperCase() || '?';
  }
  function lcCode(db, staffMember) {
    const lc = db.laborCategories.find(c => c.id === staffMember.labor_cat_id);
    return lc ? lc.code : '—';
  }
  window.LmsHelpers = {
    fmtMin,
    courseTime,
    initials,
    lcCode
  };
})();
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/water-resources-lms/helpers.js", error: String((e && e.message) || e) }); }

__ds_ns.DisclosureCard = __ds_scope.DisclosureCard;

__ds_ns.MatrixCell = __ds_scope.MatrixCell;

__ds_ns.LessonToggleCell = __ds_scope.LessonToggleCell;

__ds_ns.ResourceRow = __ds_scope.ResourceRow;

__ds_ns.Surface = __ds_scope.Surface;

__ds_ns.Avatar = __ds_scope.Avatar;

__ds_ns.CountBadge = __ds_scope.CountBadge;

__ds_ns.LaborBadge = __ds_scope.LaborBadge;

__ds_ns.LevelBadge = __ds_scope.LevelBadge;

__ds_ns.ProficiencyChip = __ds_scope.ProficiencyChip;

__ds_ns.SKILL_PROFICIENCY = __ds_scope.SKILL_PROFICIENCY;

__ds_ns.ProgressBar = __ds_scope.ProgressBar;

__ds_ns.StatusPill = __ds_scope.StatusPill;

__ds_ns.Button = __ds_scope.Button;

__ds_ns.IconButton = __ds_scope.IconButton;

__ds_ns.InlineEditText = __ds_scope.InlineEditText;

__ds_ns.Input = __ds_scope.Input;

__ds_ns.Select = __ds_scope.Select;

__ds_ns.FormField = __ds_scope.FormField;

__ds_ns.SearchBar = __ds_scope.SearchBar;

__ds_ns.NoResults = __ds_scope.NoResults;

__ds_ns.Icon = __ds_scope.Icon;

__ds_ns.GripIcon = __ds_scope.GripIcon;

__ds_ns.ICON_NAMES = __ds_scope.ICON_NAMES;

__ds_ns.Header = __ds_scope.Header;

__ds_ns.Logo = __ds_scope.Logo;

__ds_ns.PageContent = __ds_scope.PageContent;

__ds_ns.Sidebar = __ds_scope.Sidebar;

__ds_ns.Modal = __ds_scope.Modal;

__ds_ns.ModalHead = __ds_scope.ModalHead;

__ds_ns.ModalBody = __ds_scope.ModalBody;

__ds_ns.ModalFoot = __ds_scope.ModalFoot;

__ds_ns.ConfirmModal = __ds_scope.ConfirmModal;

__ds_ns.CancelButton = __ds_scope.CancelButton;

__ds_ns.PrimarySaveButton = __ds_scope.PrimarySaveButton;

__ds_ns.DangerSaveButton = __ds_scope.DangerSaveButton;

})();
