<!-- VERTICAL SLICE - NOT FOR PRODUCTION -->
<!-- Validation Question: Can a new player feel that care means observing, asking, and accepting shared cost within five minutes without guidance, and can one such loop be produced in one build day at representative quality? -->
<!-- Date: 2026-07-23 -->

# 素材来源

## AI 辅助背景

以下背景于 2026-07-23 使用 Codex 内置 `image_gen` 生成。它们是原创环境图，不使用参考图，不含人物、Logo、可读标识或官方素材。

| 文件 | 用途 | 原始生成文件 |
|---|---|---|
| `game/images/bg_rain_platform.png` | 雨夜站台 | `call_tdaZZatDLkw8GrzN2wK8Wq2e.png` |
| `game/images/bg_ticket_gate.png` | 检票口与维修门 | `call_R3d2mzGJFmy29MEOBOYSKEKZ.png` |
| `game/images/bg_train_window.png` | 列车内延迟回收 | `call_jXRUewmnp6h7ATjN0aXGPMH8.png` |

### 站台最终提示词

```text
Use case: illustration-story
Asset type: 16:9 visual-novel background for a commercial-quality vertical slice
Primary request: an original rain-soaked urban train platform at night, seen from a low eye-level three-quarter view, empty of people, with a small wet handwritten paper near a drainage channel as a subtle story focal point
Scene/backdrop: contemporary East Asian city railway platform, covered roof, tracks disappearing into a dark tunnel, distant ticket gate glow, rain blowing in from the side
Style/medium: refined hand-painted 2D background illustration, cinematic visual-novel art, painterly but readable, wholly original and not based on any existing franchise artwork
Composition/framing: wide landscape, strong depth lines toward the tunnel, clear negative space in the lower quarter for a dialogue box, important paper visible but not oversized
Lighting/mood: cold blue rain and wet reflections, restrained warm amber practical lights, tense but intimate
Color palette: navy, desaturated cyan, charcoal, small amber accents
Constraints: environment only; no people, no characters, no logos, no readable signage, no brand marks, no text, no watermark; do not imitate official Dragon Raja art or any named artist
```

### 检票口最终提示词

```text
Use case: illustration-story
Asset type: 16:9 visual-novel background for a commercial-quality vertical slice
Primary request: an original urban railway ticket-gate concourse late at night during heavy rain, empty of people, with one malfunctioning red security indicator and a sealed old maintenance door that can be noticed by an observant player
Scene/backdrop: contemporary East Asian city station interior, ticket barriers, rain visible through tall glass panels, wet footprints fading toward a corridor
Style/medium: refined hand-painted 2D background illustration, cinematic visual-novel art, painterly but spatially clear, wholly original
Composition/framing: wide landscape, ticket barriers in midground, maintenance door on the right third, clear darker lower quarter for dialogue UI
Lighting/mood: cold fluorescent blue-green light with restrained red and amber accents, suspenseful without horror gore
Color palette: slate blue, steel gray, muted cyan, tiny red indicator
Constraints: environment only; no people, no characters, no logos, no readable signage, no brand marks, no text, no watermark; do not imitate official Dragon Raja art or any named artist
```

### 列车最终提示词

```text
Use case: illustration-story
Asset type: 16:9 visual-novel background for a commercial-quality vertical slice
Primary request: an original nearly empty commuter-train interior at night in heavy rain, viewed diagonally along a row of seats toward a rain-streaked window, with two adjacent empty seats as the emotional focal point
Scene/backdrop: clean contemporary East Asian urban train car, wet city lights passing outside as soft streaks, no readable advertisements
Style/medium: refined hand-painted 2D background illustration, cinematic visual-novel art, painterly with crisp environmental storytelling, wholly original
Composition/framing: wide landscape, two adjacent seats on the right-center, rain window and receding carriage depth, uncluttered lower quarter for dialogue UI
Lighting/mood: cold blue exterior rain balanced by soft warm interior light, fragile calm after danger, intimate and hopeful without becoming cheerful
Color palette: deep navy, muted teal, warm cream, restrained rose accent from reflected city light
Constraints: environment only; no people, no characters, no logos, no readable signage, no brand marks, no text, no watermark; do not imitate official Dragon Raja art or any named artist
```

## 字体

`game/SourceHanSansLite.ttf` 来自 Ren'Py 8.5.3 SDK 的 `sdk-fonts` 目录，用于保证中文原型显示。公开发布前仍需把对应许可文本加入构建包；切片不会作为正式发布包。

