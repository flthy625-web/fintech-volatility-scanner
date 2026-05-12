"""多语言支持模块"""
import json
import streamlit as st
from pathlib import Path

# 支持的语言
LANGUAGES = {
    "zh_CN": "🇨🇳 简体中文",
    "zh_TW": "🇹🇼 繁體中文",
    "en_US": "🇺🇸 English"
}

# 翻译缓存
_translations = {}

def load_translations(lang_code):
    """加载指定语言的翻译文件"""
    if lang_code in _translations:
        return _translations[lang_code]

    locale_file = Path(__file__).parent.parent / "locales" / f"{lang_code}.json"

    try:
        with open(locale_file, 'r', encoding='utf-8') as f:
            _translations[lang_code] = json.load(f)
            return _translations[lang_code]
    except FileNotFoundError:
        # 如果文件不存在，返回简体中文作为默认
        if lang_code != "zh_CN":
            return load_translations("zh_CN")
        return {}

def get_current_language():
    """获取当前语言设置"""
    if "language" not in st.session_state:
        st.session_state.language = "zh_CN"  # 默认简体中文
    return st.session_state.language

def set_language(lang_code):
    """设置当前语言"""
    if lang_code in LANGUAGES:
        st.session_state.language = lang_code

def t(key, default=None):
    """
    翻译函数

    Args:
        key: 翻译键，支持点号分隔的嵌套键，如 "learning.title"
        default: 如果找不到翻译，返回的默认值

    Returns:
        翻译后的文本
    """
    lang = get_current_language()
    translations = load_translations(lang)

    # 支持嵌套键，如 "learning.title"
    keys = key.split('.')
    value = translations

    for k in keys:
        if isinstance(value, dict) and k in value:
            value = value[k]
        else:
            return default if default is not None else key

    return value

def render_language_selector():
    """渲染语言选择器（用于侧边栏）"""
    current_lang = get_current_language()

    st.markdown(f"### {t('language', '语言')}")

    selected = st.selectbox(
        t('select_language', '选择语言'),
        options=list(LANGUAGES.keys()),
        format_func=lambda x: LANGUAGES[x],
        index=list(LANGUAGES.keys()).index(current_lang),
        key="language_selector"
    )

    if selected != current_lang:
        set_language(selected)
        st.rerun()

def get_language_name(lang_code):
    """获取语言的显示名称"""
    return LANGUAGES.get(lang_code, "Unknown")
