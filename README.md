# Hoa Văn Cương Đạo — bản chạy trên web

Thư mục này là một bản self-host của [freej2me-web](https://github.com/zb3/freej2me-web)
(FreeJ2ME + CheerpJ), đã đóng gói sẵn game `hoa-van-cuong-dao.jar`.

## Chạy trên máy

Yêu cầu: Python 3.

```powershell
cd web
python serve.py
```

Mở trình duyệt tại **http://localhost:8000**.

> Không mở trực tiếp `index.html` bằng `file://` — CheerpJ cần HTTP server
> có hỗ trợ header `Range` (file `serve.py` đã xử lý việc này).

## Đưa lên hosting

Upload **toàn bộ nội dung thư mục `web/`** lên một static host có hỗ trợ
`Range` request, ví dụ:

- GitHub Pages
- Netlify
- Cloudflare Pages
- Vercel

Sau đó mở `https://ten-mien-cua-ban/` là chơi được.

Lưu ý:

- CheerpJ runtime được tải từ CDN `cjrtnc.leaningtech.com`, nên máy người
  chơi cần có internet.
- Không cần server backend, mọi thứ chạy trong trình duyệt.
- Nếu host không trả `206 Partial Content` cho `Range`, game sẽ tải rất chậm
  hoặc không khởi động.

## Điều khiển

| Phím | Chức năng |
|---|---|
| `↑` `↓` `←` `→` | Di chuyển |
| `Enter` | OK / chọn |
| `F1` | Phím mềm trái |
| `F2` | Phím mềm phải |
| `Esc` | Menu cài đặt của emulator |

Trên điện thoại, thêm `?mobile=1` (trang chủ tự phát hiện thiết bị cảm ứng)
để hiện bàn phím ảo.

## Cấu trúc

```
web/
├── index.html          # trang chủ / nút "Chơi ngay"
├── play.html           # trang giới thiệu (alias)
├── launcher.html       # giao diện freej2me-web gốc (cài thêm game)
├── run.html            # trang chạy game
├── serve.py            # server tĩnh có hỗ trợ Range
├── freej2me-web.jar    # emulator FreeJ2ME
├── game.jar            # bản sao game (dự phòng)
├── apps/
│   └── hvcd.zip        # bundle game: app.jar + name + config
├── libjs/              # native graphics bridge
├── libmidi/            # MIDI (fluidsynth wasm)
├── libmedia/           # media (ffmpeg wasm)
└── src/                # JS của freej2me-web
```

## Đổi cấu hình game

Giải nén `apps/hvcd.zip`, sửa `config/settings.conf` rồi nén lại (các file
phải nằm ở gốc zip, không bọc thêm thư mục):

```ini
width: 240
height: 320
sound: on
phone: Nokia
forceFullscreen: on
```

Có thể đổi `width`/`height` nếu muốn chạy ở độ phân giải khác; game sẽ tự
co giãn theo `getWidth()`/`getHeight()`.

## Ghi chú

- JAR gốc `../hoa-van-cuong-dao.jar` không bị sửa.
- Game dùng API MIDP-2.0 dù manifest ghi MIDP-1.0; FreeJ2ME chạy được bình
  thường. Nếu chạy trên máy Java thật (không phải emulator), cần sửa manifest.
- freej2me-web dùng CheerpJ (độc quyền, miễn phí cho mục đích phi thương mại)
  và FreeJ2ME (GPLv3). Kiểm tra license trước khi phát hành thương mại.
