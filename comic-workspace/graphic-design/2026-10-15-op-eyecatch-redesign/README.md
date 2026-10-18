# 魔物猎手 · 标题与中插 · 第二版

**V2 / 2026-10-15 · 源码交付。** 仓库仅提交动画、音效合成、渲染脚本、静态 SVG 素材和说明。成品 MOV / MP4 / WAV、PNG 序列、栅格缓存和 QA 图片均在本地生成，不提交到 Git。

## 第二版内容

- 供现有 OP 叠加的 5 秒透明圆环标题：展开、字形环绕、汇聚、停留、回环退场。
- 两段各 4 秒的中插：文字沿弧线入场，去掉巨大淡色背景字、两侧独立 ♂／♀ 与上下英文。
- 两段原创合成音效：空气扫掠、文字触点、晶体、低频与空间五层。48kHz / 24-bit 立体声。

第一版保留在同级 `2026-10-14-blue-style/`。本目录已包含可直接重建的 SVG，不需要下载第一版视频或 LFS 成品。

## 在其他电脑重建

准备 Node.js 20+、Python 3.10+、Google Chrome 和支持 libx264 / prores_ks 的 FFmpeg。以下命令均在本目录执行：

```sh
npm install
python -m pip install -r requirements.txt
npm run build
```

脚本默认从系统 PATH 调用 `ffmpeg`、`python`，通过 Playwright 的 `chrome` channel 使用已安装的 Google Chrome。也可指定环境变量 `FFMPEG_PATH`、`PYTHON`、`CHROME_PATH`，其值为各程序的完整路径。兼容本地 `package/ffmpeg.exe`（Windows）或 `package/ffmpeg`，工具本身不入库。

`npm run build` 依次完成 SVG 栅格化 → 声音合成与母带 → 中插 4K / 1080p → 透明标题 → 总览与最终音轨。标题会渲染 300 张 4K PNG 并编码 ProRes，需要较多时间和数 GB 可用空间。

分步运行：

```sh
npm run assets
npm run check
npm run sound
npm run render:eyes
npm run render:title
node finalize-title-delivery.cjs
node attach_eyecatch_sound.cjs
```

`npm run check` 验证素材加载、关键帧透明度、A/B 衔接和浏览器 H.264 编码能力。若浏览器不支持 WebCodecs H.264 编码，请通过 `CHROME_PATH` 指定支持该能力的 Google Chrome。

完成栅格化后，可运行 `python -m http.server 4188 --bind 127.0.0.1`，打开 `http://127.0.0.1:4188/index.html` 查看实时动画；`title-overlay.html` 提供标题透明背景预览。音效生成后，实时预览可播放声音；完整渲染后，`watch.html` 可播放成片。

## 本地生成的交付文件

- `exports/Title-overlay-4K60-alpha.mov`、`Title-overlay-1080p60-alpha.mov`：5 秒透明 ProRes 4444，无音轨，首尾全透明。
- `exports/Eyecatch-A-break-{4K60,1080p60}.mp4`、`Eyecatch-B-continue-{4K60,1080p60}.mp4`：各 4 秒，带最终音效。
- `exports/Current-deliverables-preview-1080p60.mp4`：标题 5 秒 + A 4 秒 + B 4 秒。
- `audio/sound-design-v1/*-master-48k24.wav` 与 `stems/`：音效母版及五层分轨。
- `qa/`：关键帧图与校验报告。

动画时间轴在 `motion.js`；声音合成在 `design_eyecatch_sfx.py`。其他说明见[标题叠加说明](标题叠加说明.md)、[中插修订记录](中插修订记录.md)、[中插音效说明](中插音效说明.md)。`delivery-manifest.json` 保留本次本机成品校验值供核对，不表示成品已纳入 Git；浏览器和编码器版本不同可能影响重新编码后的文件哈希。
