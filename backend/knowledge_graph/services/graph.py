from typing import List, Dict, Any, Optional, Set
from sqlalchemy.orm import Session
from ..models.relationships import Entity, EntityRelationship
from ..core.logger import logger

class GraphService:
    def __init__(self, db: Session):
        self.db = db
        
    def get_entity_with_relations(self, entity_id: int, depth: int = 1) -> Dict[str, Any]:
        """获取实体及其关系网络"""
        try:
            entity = self.db.query(Entity).filter(Entity.id == entity_id).first()
            if not entity:
                return None
                
            visited = {entity_id}  # 已访问的节点
            graph = {
                "nodes": [self._entity_to_dict(entity)],
                "links": []
            }
            
            if depth > 0:
                self._get_related_entities(entity_id, depth, visited, graph)
                
            return graph
        except Exception as e:
            logger.error(f"获取实体关系网络失败: {str(e)}")
            raise
            
    def _get_related_entities(
        self, 
        entity_id: int, 
        depth: int, 
        visited: Set[int], 
        graph: Dict[str, List]
    ) -> None:
        """递归获取相关实体"""
        if depth <= 0:
            return
            
        # 获取所有相关关系
        relationships = self.db.query(EntityRelationship).filter(
            (EntityRelationship.source_id == entity_id) |
            (EntityRelationship.target_id == entity_id)
        ).all()
        
        for rel in relationships:
            # 确定目标实体
            target_id = rel.target_id if rel.source_id == entity_id else rel.source_id
            
            # 如果目标实体未访问过
            if target_id not in visited:
                visited.add(target_id)
                target_entity = self.db.query(Entity).filter(Entity.id == target_id).first()
                
                if target_entity:
                    # 添加节点
                    graph["nodes"].append(self._entity_to_dict(target_entity))
                    # 递归获取更深层的关系
                    self._get_related_entities(target_id, depth - 1, visited, graph)
            
            # 添加关系
            graph["links"].append({
                "source": rel.source_id,
                "target": rel.target_id,
                "type": rel.relationship_type,
                "properties": rel.properties
            })
    
    def get_shortest_path(
        self, 
        source_id: int, 
        target_id: int, 
        max_depth: int = 5
    ) -> Optional[List[Dict[str, Any]]]:
        """查找两个实体之间的最短路径"""
        try:
            # 使用广度优先搜索
            queue = [(source_id, [{"id": source_id}])]
            visited = {source_id}
            
            while queue and len(visited) < max_depth * 100:  # 限制搜索范围
                current_id, path = queue.pop(0)
                
                # 获取当前节点的所有关系
                relationships = self.db.query(EntityRelationship).filter(
                    (EntityRelationship.source_id == current_id) |
                    (EntityRelationship.target_id == current_id)
                ).all()
                
                for rel in relationships:
                    next_id = rel.target_id if rel.source_id == current_id else rel.source_id
                    
                    if next_id == target_id:
                        # 找到目标节点，返回路径
                        return path + [
                            {
                                "relationship": rel.relationship_type,
                                "properties": rel.properties
                            },
                            {"id": next_id}
                        ]
                    
                    if next_id not in visited and len(path) < max_depth * 2:
                        visited.add(next_id)
                        new_path = path + [
                            {
                                "relationship": rel.relationship_type,
                                "properties": rel.properties
                            },
                            {"id": next_id}
                        ]
                        queue.append((next_id, new_path))
            
            return None  # 未找到路径
            
        except Exception as e:
            logger.error(f"查找最短路径失败: {str(e)}")
            raise
    
    def get_subgraph(
        self, 
        entity_ids: List[int], 
        include_relations: bool = True
    ) -> Dict[str, Any]:
        """获取多个实体构成的子图"""
        try:
            # 获取所有指定的实体
            entities = self.db.query(Entity).filter(Entity.id.in_(entity_ids)).all()
            graph = {
                "nodes": [self._entity_to_dict(entity) for entity in entities],
                "links": []
            }
            
            if include_relations:
                # 获取这些实体之间的所有关系
                relationships = self.db.query(EntityRelationship).filter(
                    (EntityRelationship.source_id.in_(entity_ids)) &
                    (EntityRelationship.target_id.in_(entity_ids))
                ).all()
                
                graph["links"] = [
                    {
                        "source": rel.source_id,
                        "target": rel.target_id,
                        "type": rel.relationship_type,
                        "properties": rel.properties
                    }
                    for rel in relationships
                ]
            
            return graph
            
        except Exception as e:
            logger.error(f"获取子图失败: {str(e)}")
            raise
    
    @staticmethod
    def _entity_to_dict(entity: Entity) -> Dict[str, Any]:
        """将实体对象转换为字典"""
        return {
            "id": entity.id,
            "name": entity.name,
            "type": entity.entity_type,
            "description": entity.description,
            "properties": entity.properties,
            "status": entity.status
        } 