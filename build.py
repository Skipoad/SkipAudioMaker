import os
import platform
import shutil
import PyInstaller.__main__
import sys

def build_application():
    # 清理之前的构建
    print("清理之前的构建...")
    shutil.rmtree('build', ignore_errors=True)
    shutil.rmtree('dist', ignore_errors=True)
    
    # 平台特定配置
    system = platform.system()
    icon_path = None
    
    if system == 'Windows':
        icon_path = 'assets/icons/app_icon.ico'
    elif system == 'Darwin':  # macOS
        icon_path = 'assets/icons/app_icon.icns'
    else:  # Linux
        icon_path = 'assets/icons/app_icon.png'
    
    # 创建构建参数
    args = [
        'main.py',
        '--name=SkipAudioMaker',
        '--onefile',
        '--windowed',
        '--add-data=assets;assets',
    ]
    
    # 添加图标参数
    if icon_path and os.path.exists(icon_path):
        args.append(f'--icon={icon_path}')
    else:
        print(f"警告: 图标文件未找到: {icon_path}")
    
    # 添加 macOS 特定选项
    if system == 'Darwin':
        args.extend([
            '--osx-bundle-identifier=com.yourcompany.skipaudiomaker',
            '--target-arch=x86_64,arm64'  # 支持 Apple Silicon
        ])
    
    # 运行打包
    print("开始打包应用程序...")
    PyInstaller.__main__.run(args)
    
    # 复制额外的资源文件
    print("复制资源文件...")
    if system == 'Darwin':
        # macOS 特殊处理
        app_path = 'dist/SkipAudioMaker.app'
        resources_path = os.path.join(app_path, 'Contents', 'Resources')
        if not os.path.exists(resources_path):
            os.makedirs(resources_path, exist_ok=True)
        if os.path.exists('assets'):
            shutil.copytree('assets', os.path.join(resources_path, 'assets'), dirs_exist_ok=True)
    else:
        # Windows/Linux
        assets_dest = os.path.join('dist', 'assets')
        if os.path.exists(assets_dest):
            shutil.rmtree(assets_dest)
        shutil.copytree('assets', assets_dest)
    
    print("\n构建完成！应用程序在 'dist' 目录中")

if __name__ == "__main__":
    build_imports()