import mysql.connector

class DBHelper:
    def __init__(self):
        # 数据库配置
        self.config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'zyf52LZX1314',  # 替换为你的密码
            'database': 'image_editor_app'
        }

    def connect(self):
        """
        建立并返回一个数据库连接。
        """
        return mysql.connector.connect(**self.config)

    # -------------------------------------
    # 1️⃣ 原有的操作步骤相关表 edit_steps
    # -------------------------------------
#存储图片以及步骤
    def save_edit_step(self, user_id, step_order, image_data):
        """
        保存用户的一步编辑操作到 edit_steps 表。
        """
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO edit_steps (user_id, step_order, image_data) VALUES (%s, %s, %s)',
            (user_id, step_order,image_data)
        )
        conn.commit()
        cursor.close()
        conn.close()

    def get_user_steps(self, user_id):
        """
        获取某用户的所有历史操作步骤，按 step_order 排序。
        """
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM edit_steps WHERE user_id=%s ORDER BY step_order', (user_id,))
        steps = cursor.fetchall()
        cursor.close()
        conn.close()
        return steps

    def undo_last_step(self, user_id):
        """
        撤销用户的最后一步操作（删除最后一条记录）。
        """
        conn = self.connect()
        cursor = conn.cursor()
        # 通过子查询找到最后一步的 id，然后删除
        cursor.execute(
            'DELETE FROM edit_steps WHERE id= (SELECT id2 FROM (SELECT id AS id2 FROM edit_steps WHERE user_id=%s ORDER BY step_order DESC LIMIT 1) t)',
            (user_id,)
        )
        conn.commit()
        cursor.close()
        conn.close()

    def clear_steps(self, user_id):
        """
        删除该用户的所有操作步骤（通常在重新上传图片时调用）。
        """
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM edit_steps WHERE user_id=%s', (user_id,))
        conn.commit()
        cursor.close()
        conn.close()

    def get_last_image(self, user_id):
        """
        获取该用户最新保存的图像二进制数据（最新一步）。
        返回: image_data (bytes)，若不存在则返回 None
        """
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT image_data FROM edit_steps WHERE user_id=%s ORDER BY step_order DESC LIMIT 1',
            (user_id,)
        )
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        if result:
            return result[0]  # image_data
        else:
            return None