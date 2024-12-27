"""数据库工具模块"""
import sqlite3
from typing import List, Dict, Any, Optional, Union
from contextlib import contextmanager

class Database:
    """数据库工具类"""
    
    def __init__(self, db_path: str):
        """初始化数据库连接
        
        Args:
            db_path: 数据库文件路径
        """
        self.db_path = db_path
        self._conn = None
        
    def _get_connection(self) -> sqlite3.Connection:
        """获取数据库连接"""
        if self._conn is None:
            self._conn = sqlite3.connect(self.db_path)
            self._conn.row_factory = sqlite3.Row
        return self._conn
        
    def close(self):
        """关闭数据库连接"""
        if self._conn is not None:
            self._conn.close()
            self._conn = None
            
    @contextmanager
    def transaction(self):
        """事务上下文管理器"""
        conn = self._get_connection()
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
            
    def execute(self, query: str, params: Union[tuple, dict] = ()) -> List[Dict[str, Any]]:
        """执行SQL查询
        
        Args:
            query: SQL查询语句
            params: 查询参数，可以是元组或字典
            
        Returns:
            查询结果列表
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        
        if query.strip().upper().startswith('SELECT'):
            return [dict(row) for row in cursor.fetchall()]
        else:
            conn.commit()
            return []
                
    def execute_many(self, query: str, params_list: List[Union[tuple, dict]]) -> bool:
        """批量执行SQL查询
        
        Args:
            query: SQL查询语句
            params_list: 参数列表
            
        Returns:
            是否执行成功
        """
        try:
            with self.transaction() as conn:
                cursor = conn.cursor()
                cursor.executemany(query, params_list)
                return True
        except Exception:
            return False
                
    def execute_script(self, script: str) -> bool:
        """执行SQL脚本
        
        Args:
            script: SQL脚本
            
        Returns:
            是否执行成功
        """
        try:
            with self.transaction() as conn:
                conn.executescript(script)
                return True
        except Exception:
            return False
                
    def get_by_id(self, table: str, id_value: int) -> Optional[Dict[str, Any]]:
        """根据ID获取记录
        
        Args:
            table: 表名
            id_value: ID值
            
        Returns:
            记录字典，如果不存在则返回None
        """
        result = self.execute(f"SELECT * FROM {table} WHERE id = ?", (id_value,))
        return result[0] if result else None
        
    def insert(self, table: str, data: Dict[str, Any]) -> Optional[int]:
        """插入记录
        
        Args:
            table: 表名
            data: 记录数据
            
        Returns:
            插入记录的ID，如果失败则返回None
        """
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        
        try:
            with self.transaction() as conn:
                cursor = conn.cursor()
                cursor.execute(query, tuple(data.values()))
                return cursor.lastrowid
        except Exception:
            return None
                
    def update(self, table: str, id_value: int, data: Dict[str, Any]) -> bool:
        """更新记录
        
        Args:
            table: 表名
            id_value: ID值
            data: 更新数据
            
        Returns:
            是否更新成功
        """
        set_clause = ', '.join([f"{k} = ?" for k in data.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE id = ?"
        params = tuple(data.values()) + (id_value,)
        
        try:
            with self.transaction() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                return True
        except Exception:
            return False
                
    def delete(self, table: str, id_value: int) -> bool:
        """删除记录
        
        Args:
            table: 表名
            id_value: ID值
            
        Returns:
            是否删除成功
        """
        try:
            with self.transaction() as conn:
                cursor = conn.cursor()
                cursor.execute(f"DELETE FROM {table} WHERE id = ?", (id_value,))
                return True
        except Exception:
            return False
                
    def table_exists(self, table: str) -> bool:
        """检查表是否存在
        
        Args:
            table: 表名
            
        Returns:
            表是否存在
        """
        result = self.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name=?
        """, (table,))
        return bool(result)
        
    def get_table_info(self, table: str) -> List[Dict[str, Any]]:
        """获取表结构信息
        
        Args:
            table: 表名
            
        Returns:
            表结构信息列表
        """
        return self.execute(f"PRAGMA table_info({table})")
        
    def begin_transaction(self):
        """开始事务"""
        conn = self._get_connection()
        conn.execute("BEGIN")
            
    def commit_transaction(self):
        """提交事务"""
        if self._conn is not None:
            self._conn.commit()
            
    def rollback_transaction(self):
        """回滚事务"""
        if self._conn is not None:
            self._conn.rollback()
