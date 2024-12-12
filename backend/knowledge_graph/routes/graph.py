from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, Query, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.graph import GraphService
from ..core.deps import get_current_user
from ..core.logger import logger

router = APIRouter(prefix="/graph", tags=["graph"])

@router.get("/entity/{entity_id}/network")
async def get_entity_network(
    entity_id: int,
    depth: int = Query(1, ge=1, le=3),
    db: Session = Depends(get_db)
):
    """获取实体的关系网络"""
    try:
        graph_service = GraphService(db)
        network = graph_service.get_entity_with_relations(entity_id, depth)
        
        if not network:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="实体不存在"
            )
            
        return network
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取实体网络失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取实体网络失败: {str(e)}"
        )

@router.get("/path")
async def find_shortest_path(
    source_id: int,
    target_id: int,
    max_depth: int = Query(5, ge=1, le=10),
    db: Session = Depends(get_db)
):
    """查找两个实体之间的最短路径"""
    try:
        graph_service = GraphService(db)
        path = graph_service.get_shortest_path(source_id, target_id, max_depth)
        
        if not path:
            return {"message": "未找到连接路径"}
            
        return {"path": path}
    except Exception as e:
        logger.error(f"查找最短路径失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"查找最短路径失败: {str(e)}"
        )

@router.get("/subgraph")
async def get_subgraph(
    entity_ids: List[int] = Query(...),
    include_relations: bool = True,
    db: Session = Depends(get_db)
):
    """获取多个实体构成的子图"""
    try:
        if len(entity_ids) > 100:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="实体数量不能超过100个"
            )
            
        graph_service = GraphService(db)
        subgraph = graph_service.get_subgraph(entity_ids, include_relations)
        return subgraph
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取子图失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取子图失败: {str(e)}"
        )

@router.get("/recommend/{entity_id}")
async def get_recommended_entities(
    entity_id: int,
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """获取推荐的相关实体"""
    try:
        graph_service = GraphService(db)
        # 获取两层深度的关系网络
        network = graph_service.get_entity_with_relations(entity_id, depth=2)
        
        if not network:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="实体不存在"
            )
        
        # 简单的推荐算法：返回与当前实体有直接或间接关系的实体
        # 可以根据关系类型、属性等进行更复杂的推荐
        recommended = []
        visited = {entity_id}
        
        for link in network["links"]:
            source_id = link["source"]
            target_id = link["target"]
            
            if source_id == entity_id and target_id not in visited:
                for node in network["nodes"]:
                    if node["id"] == target_id:
                        recommended.append(node)
                        visited.add(target_id)
                        break
            elif target_id == entity_id and source_id not in visited:
                for node in network["nodes"]:
                    if node["id"] == source_id:
                        recommended.append(node)
                        visited.add(source_id)
                        break
                        
            if len(recommended) >= limit:
                break
        
        return {"recommended": recommended[:limit]}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取推荐实体失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取推荐实体失败: {str(e)}"
        ) 