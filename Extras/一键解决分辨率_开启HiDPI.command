#!/bin/bash
# ========================================================
# 机械革命无界 14 Pro - 屏幕分辨率与 HiDPI 视网膜缩放优化工具
# Screen Resolution & HiDPI Optimizer
# ========================================================

clear
echo "=========================================================="
echo "   无界 14 Pro 屏幕分辨率与 HiDPI 黄金视网膜缩放工具"
echo "=========================================================="
echo " 屏幕硬件规格: 14.0 英寸 2880 × 1800 (16:10 黄金比例)"
echo " 推荐最佳缩放: 1920 × 1200 (HiDPI 视网膜大字体)"
echo "=========================================================="
echo ""
echo "请选择操作："
echo " 1) 修复 BetterDisplay（清除隔离属性，解决秒退/无法打开）"
echo " 2) 清理 WindowServer 屏幕缓存（解决改分辨率导致的黑屏/死锁）"
echo " 3) 运行国内 Gitee 一键 HiDPI 脚本（免常驻后台，开启原生 5 档缩放）"
echo " 4) 全套一键体检与清理（执行 1 + 2）"
echo " 0) 退出"
echo ""
read -p "请输入选项 [0-4]: " choice

case "$choice" in
    1)
        echo ""
        echo "[*] 正在解除 BetterDisplay 隔离属性..."
        if [ -d "/Applications/BetterDisplay.app" ]; then
            sudo xattr -cr /Applications/BetterDisplay.app
            echo "[OK] 已成功解除隔离！现在可以正常双击打开 BetterDisplay。"
        else
            echo "[!] 应用程序中未找到 BetterDisplay.app，请先将应用拖入【应用程序】目录。"
        fi
        ;;
    2)
        echo ""
        echo "[*] 正在彻底清除 WindowServer 遗留的显示器与分辨率脏配置..."
        sudo rm -f /Library/Preferences/com.apple.windowserver.displays.plist
        rm -f ~/Library/Preferences/ByHost/com.apple.windowserver.displays.*.plist
        echo "[OK] 脏配置文件已清空！重启系统后将自动按最佳默认分辨率初始化。"
        ;;
    3)
        echo ""
        echo "[*] 正在从 Gitee 极速下载并运行 one-key-hidpi 脚本..."
        bash -c "$(curl -fsSL https://gitee.com/xzhih/one-key-hidpi/raw/master/hidpi.sh)"
        ;;
    4)
        echo ""
        echo "[*] 正在解除 BetterDisplay 隔离属性..."
        [ -d "/Applications/BetterDisplay.app" ] && sudo xattr -cr /Applications/BetterDisplay.app
        echo "[*] 正在清空脏显示配置..."
        sudo rm -f /Library/Preferences/com.apple.windowserver.displays.plist
        rm -f ~/Library/Preferences/ByHost/com.apple.windowserver.displays.*.plist
        echo "[OK] 全部清理完成！"
        ;;
    0)
        exit 0
        ;;
    *)
        echo "无效选项！"
        ;;
esac

echo ""
read -p "按回车键退出..."
