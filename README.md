# 机械革命无界 14XA · macOS Tahoe EFI

适用于 WUJIE14XA（WUJIE14-GX4HRXL）、Ryzen 7 8845HS、Radeon 780M、Intel AX200。基于 OpenCore 1.0.8 DEBUG，目标系统为 macOS Tahoe 26.7.3。

| 功能 | 本机验证状态 |
| --- | --- |
| macOS 启动、NullArc 显示驱动安装、I²C 触控板 | 已在 14XA 上确认 |
| AX200 Wi‑Fi 和蓝牙、CX8070 扬声器与耳机输出、USB 鼠标 | 已在 14XA 上实测正常 |
| 电池读数 | 当前 ACPI 诊断配置下停用 |

## 生成并使用 EFI

1. 下载或克隆仓库，在仓库目录用 Python 3 运行 `python assemble-efi.py`。脚本从组件清单中的发行地址获取驱动，核对 SHA‑256，再生成 `WUJIE14XA-EFI.zip`。有现用 EFI 的用户可以通过 `--source-efi` 指定该 EFI 目录来离线组装。
2. 解压生成的 ZIP，在 `EFI/OC/config.plist` 的 `PlatformInfo → Generic` 为 `MacBookPro16,1` 填写自己生成的 `SystemSerialNumber`、`MLB`、`SystemUUID` 和 `ROM`。公开配置中的身份字段使用空值或全零占位。
3. 使用 OpenCore 1.0.8 自带的 `ocvalidate` 检查配置，然后将 `EFI` 放到一个 FAT32 U 盘根目录进行试启动。保留原来能启动的 EFI，从 U 盘进入 OpenCore 后选择已安装的 macOS 系统卷。
4. 首次安装 NullArc 时先运行上游的 `sudo ./install.sh --check`。通过后按照对应版本的安装说明安装用户态组件。此配置会放宽 SIP 和 AMFI 防护。[NullArc 0.4.0-alpha](https://github.com/luuumi-dev/nullarc/releases/tag/v0.4.0-alpha)

## HiDPI

在 macOS 上打开 `Extras/一键解决分辨率_开启HiDPI.command`，也可用 `bash` 运行。菜单包含 BetterDisplay 隔离属性处理、WindowServer 显示配置重置以及下载并执行上游 one-key-hidpi。脚本内的分辨率提示来自 14 Pro，应以本机屏幕实际支持的设置为准。[原脚本](https://github.com/bbbbrt/mechrevo-wujie14pro-7840hs-780m-hackintosh-efi/blob/d631f900a4eb36012ab6ba247eb48122b8600c3c/scripts/%E4%B8%80%E9%94%AE%E8%A7%A3%E5%86%B3%E5%88%86%E8%BE%A8%E7%8E%87_%E5%BC%80%E5%90%AFHiDPI.command)

## 组件来源

`components.json` 记录第三方组件的发行地址和 SHA‑256。驱动遵循各自上游许可。HiDPI 脚本来自 bbbbrt 的 14 Pro 项目，随附其 [MIT 许可证](licenses/HiDPI-MIT.txt)。CPU 内核补丁基于 [AMD Vanilla](https://github.com/AMD-OSX/AMD_Vanilla)，包含适配 8 核和 Tahoe 的设置。
