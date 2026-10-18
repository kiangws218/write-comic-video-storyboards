const fs = require('fs');
const path = require('path');
const localFFmpeg = path.join(__dirname, 'package', process.platform === 'win32' ? 'ffmpeg.exe' : 'ffmpeg');
exports.ffmpeg = process.env.FFMPEG_PATH || (fs.existsSync(localFFmpeg) ? localFFmpeg : 'ffmpeg');
exports.browserOptions = process.env.CHROME_PATH ? { executablePath: process.env.CHROME_PATH } : { channel: 'chrome' };
