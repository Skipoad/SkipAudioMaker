class BrandColors:
    PRIMARY = "#4682B4"  # 钢蓝色
    SECONDARY = "#48D1CC"  # 青色
    ACCENT = "#FF6347"  # 番茄红
    BACKGROUND = "#2C3E50"  # 深蓝灰
    TEXT = "#ECF0F1"  # 浅灰
    
    @staticmethod
    def get_stylesheet():
        """生成品牌CSS样式表"""
        return f"""
            /* 全局样式 */
            QWidget {{
                background-color: {BrandColors.BACKGROUND};
                color: {BrandColors.TEXT};
                font-family: "Arial", sans-serif;
                font-size: 12px;
            }}
            
            /* 主窗口 */
            QMainWindow {{
                background-color: {BrandColors.BACKGROUND};
            }}
            
            /* 工具栏 */
            QToolBar {{
                background-color: #34495E;
                border-bottom: 1px solid {BrandColors.PRIMARY};
                padding: 5px;
                spacing: 5px;
            }}
            
            QToolButton {{
                background-color: {BrandColors.PRIMARY};
                color: white;
                border-radius: 4px;
                padding: 5px;
                min-width: 32px;
                min-height: 32px;
            }}
            
            QToolButton:hover {{
                background-color: {BrandColors.SECONDARY};
            }}
            
            /* 按钮 */
            QPushButton {{
                background-color: {BrandColors.PRIMARY};
                color: white;
                border-radius: 4px;
                padding: 5px 10px;
                border: none;
            }}
            
            QPushButton:hover {{
                background-color: {BrandColors.SECONDARY};
            }}
            
            QPushButton:pressed {{
                background-color: #1F618D;
            }}
            
            /* 标签 */
            QLabel {{
                color: {BrandColors.TEXT};
            }}
            
            /* 列表视图 */
            QListWidget {{
                background-color: #34495E;
                border: 1px solid {BrandColors.PRIMARY};
                border-radius: 4px;
                color: {BrandColors.TEXT};
            }}
            
            /* 输入框 */
            QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {{
                background-color: #34495E;
                color: {BrandColors.TEXT};
                border: 1px solid {BrandColors.PRIMARY};
                border-radius: 4px;
                padding: 5px;
            }}
            
            /* 停靠窗口 */
            QDockWidget {{
                background-color: {BrandColors.BACKGROUND};
                border: 1px solid {BrandColors.PRIMARY};
                border-radius: 4px;
            }}
            
            QDockWidget::title {{
                background-color: {BrandColors.PRIMARY};
                padding: 5px;
                text-align: center;
                color: white;
            }}
        """