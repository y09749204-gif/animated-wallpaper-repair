# Animated Wallpaper Repair

一个用于修复分层 HTML/canvas 动态壁纸的 Codex skill。重点是运动发丝、下巴与固定脖颈的遮挡、眨眼残线、贴图接缝，以及整帧闪白。它不会附带或生成角色原画。

将整个仓库目录放在 Codex 的 skills 目录下，然后在任务中使用 `$animated-wallpaper-repair`，例如：“用 `$animated-wallpaper-repair` 查明摇头时的颈侧接缝并修复。”Codex 也可在匹配的任务中自动选用它。

仓库内容：

- `SKILL.md`：诊断、最小修复及预览/桌面验收流程。
- `references/illustration-to-wallpaper-case.md`：一个实际项目的制作过程和失败教训；仅在相关任务中阅读。
- `scripts/verify_pixel_scope.py`：核对 PNG 改动没有越出指定矩形，默认也不允许 alpha 变化。
- `tests/`：像素检查脚本的单元测试。

像素校验工具需要 Python 和 Pillow：

```bash
python -m pip install -r requirements.txt
python scripts/verify_pixel_scope.py before.png after.png --roi 100 200 40 60
python -m unittest discover -s tests -v
```

`--roi` 使用**源贴图**像素坐标，不是浏览器截图坐标。非矩形修改应按实际蒙版另行验证。工具只读输入文件，输出 JSON；范围外有改动或未经允许的 alpha 改动时返回非零退出码。

公开仓库不包含原画、眼帧、音乐、Wallpaper Engine 工程、账户信息或创意工坊 ID。案例的项目授权不适用于其他作品；公开发布壁纸及其素材须逐项目确认权利。
