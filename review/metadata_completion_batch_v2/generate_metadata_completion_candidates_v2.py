#!/usr/bin/env python3
"""全库缺注释字段+缺表注释候选生成脚本 V2。
基于字段名、同表已有注释、数据类型、表名语义推断。
不执行 SQL，不修改数据库。
"""

import csv
import os
import re
from collections import defaultdict

BASE = r"E:\3\code\metadata_audit"
OUT_DIR = os.path.join(BASE, "review", "metadata_completion_batch_v2")
os.makedirs(OUT_DIR, exist_ok=True)

# ---- 读取数据 ----
def load_pipe(path, cols):
    rows = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) >= cols:
                rows.append(parts)
    return rows

# 已有字段注释: schema|table|column|type|comment
existing_cols = load_pipe(r"E:\3\code\temp_existing_comments.txt", 5)
existing_table_comments = load_pipe(r"E:\3\code\temp_existing_table_comments.txt", 3)

# 缺字段注释: schema|table|column|type|attnum
missing_cols = load_pipe(r"E:\3\code\temp_missing_cols.txt", 5)
# 缺表注释: schema|table
missing_tables = load_pipe(r"E:\3\code\temp_missing_tables.txt", 2)

# ---- 构建索引 ----
# table -> {column: comment}
existing_by_table = defaultdict(dict)
for parts in existing_cols:
    table = parts[1]
    col = parts[2]
    comment = parts[4] if len(parts) > 4 else ''
    existing_by_table[table][col] = comment

# table -> table_comment
existing_table_cmt = {}
for parts in existing_table_comments:
    table = parts[1]
    cmt = parts[2] if len(parts) > 2 else ''
    existing_table_cmt[table] = cmt

# ---- 通用模式表 ----
# 标准审计字段：几乎所有表都有，注释固定
AUDIT_FIELDS = {
    'create_by': '创建人',
    'create_time': '创建时间',
    'update_by': '修改人',
    'update_time': '修改时间',
    'update_date': '修改日期',
    'create_date': '创建日期',
    'del_flag': '删除标志：0-正常，1-已删除',
    'del_status': '删除状态',
}

# 通用 ID 字段
ID_FIELDS = {
    'id': '主键ID',
    'gid': '地理要素唯一标识',
    'objectid': '对象唯一标识',
    'OBJECTID': '对象唯一标识',
    'region_id': '区域ID',
    'parent_id': '父级ID',
    'asset_id': '资产ID',
    'source_asset_id': '源资产ID',
    'from_node_id': '上游节点ID',
    'to_node_id': '下游节点ID',
    'snap_node_id': '吸附节点ID',
    'snap_edge_id': '吸附边ID',
    'node_id': '节点ID',
    'edge_id': '边ID',
    'control_unit_id': '管控单元ID',
}

# 几何字段
GEOM_FIELDS = {
    'geom': '空间几何数据',
}

# 通用字段（跨表高频）
COMMON_FIELDS = {
    'name': '名称',
    'code': '编码',
    'type': '类型',
    'remark': '备注',
    'address': '地址',
    'status': '状态',
    'level': '级别',
    'x': 'X坐标',
    'y': 'Y坐标',
    'length': '长度',
    'width': '宽度',
    'population': '人口数量',
    'year': '年份',
    'srid': '空间参考标识符',
    'srtext': '空间参考系WKT描述',
    'proj4text': '空间参考系Proj4描述',
    'auth_name': '空间参考系授权机构名称',
    'auth_srid': '空间参考系授权机构SRID',
}

# 通用字段（中置信度）
COMMON_FIELDS_MID = {
    'area': '面积',
    'total_area': '总面积',
    'core_area': '核心区面积',
    'buffer_area': '缓冲区面积',
    'shape_leng': '要素长度',
    'shape_area': '要素面积',
    'poly_area': '多边形面积',
    'period': '时期/阶段',
    'bas': '流域编码',
    'cc': '行政区划编码',
    'gb': '国标编码',
    'ec': '生态分区编码',
    'wq': '水质类别',
    'shrc': '所属河湖编码',
    'sdtf': '水系特征码',
    'featid': '要素唯一标识',
    'elemstime': '要素起始时间',
    'elemetime': '要素终止时间',
    'ecrm': '生态红线管理编号',
    'wrid': '水资区划ID',
    'wrgr': '水资区划分组',
    'areacode': '行政区划代码',
    'changetype': '变更类型',
    'changeatt': '变更属性',
    'vol': '库容',
    'aheight': '坝高',
    'mheight': '最大坝高',
    'parea': '永久占地面积',
    'grade': '等级/级别',
    'country': '国家',
    'aliasname': '别名',
    'LayerName': '图层名称',
    'LayerType': '图层类型',
}

# ---- 域分类 ----
def classify_table(table_name):
    """基于表名前缀分类"""
    table_lower = table_name.lower()
    # _stg 临时表
    if table_lower.startswith('_stg'):
        return 'staging'
    if table_lower.startswith('stg_'):
        return 'staging'
    # spatial_ref_sys
    if table_name == 'spatial_ref_sys':
        return 'postgis_system'
    # gis_ 前缀
    if table_lower.startswith('gis_'):
        return 'gis'
    # layer_ 前缀
    if table_lower.startswith('layer_'):
        return 'layer'
    # wm_ 前缀（水环境监测相关）
    if table_lower.startswith('wm_'):
        return 'water_monitor'
    # wh_ 前缀（气象/水文）
    if table_lower.startswith('wh_'):
        return 'weather_hydro'
    # wst_ 前缀（水环境溯源）
    if table_lower.startswith('wst_'):
        return 'water_trace'
    # rs_ 前缀（遥感）
    if table_lower.startswith('rs_'):
        return 'remote_sensing'
    # se_ 前缀
    if table_lower.startswith('se_'):
        return 'social_economic'
    # ad_ 前缀（字典）
    if table_lower.startswith('ad_'):
        return 'admin_dict'
    # metadata_view
    if table_lower == 'metadata_view':
        return 'metadata_view'
    # day_quality_setting
    if table_lower == 'day_quality_setting':
        return 'quality_setting'
    return 'other'

# ---- 表注释候选生成 ----
def generate_table_comment(table_name, domain):
    """基于表名和域分类生成表注释候选"""
    table_lower = table_name.lower()

    # GIS 表
    if domain == 'gis':
        if 'ecologicalregion' in table_lower:
            return '生态保护红线区域表', 'auto_safe'
        if 'headwaters' in table_lower:
            return '水源地表', 'auto_safe'
        if 'naturereserve' in table_lower:
            return '自然保护区表', 'auto_safe'
        if 'region_population' in table_lower:
            return '行政区人口统计表', 'auto_safe'
        if 'region_city' in table_lower:
            return '城市行政区划表', 'auto_safe'
        if 'region_county' in table_lower:
            return '区县行政区划表', 'auto_safe'
        if 'region_township' in table_lower:
            return '乡镇行政区划表', 'auto_safe'
        if 'region' in table_lower:
            return '行政区划表', 'auto_safe'
        if 'watershed_partition_4' in table_lower:
            return '四级流域分区表', 'auto_safe'
        if 'watershed_partition_3' in table_lower:
            return '三级流域分区表', 'auto_safe'
        if 'watershed_partition' in table_lower:
            return '流域分区表', 'auto_safe'
        if 'control_unit' in table_lower:
            return '水环境管控单元表', 'auto_safe'
        if 'poi' in table_lower:
            return 'POI点位信息表', 'auto_safe'

    # Layer 表
    if domain == 'layer':
        if 'reservoir_provincial_label' in table_lower:
            return '省级水库标注点表', 'auto_safe'
        if 'reservoir_provincial' in table_lower:
            return '省级水库空间表', 'auto_safe'
        if 'river_provincial' in table_lower:
            return '省级河流空间表', 'auto_safe'
        if 'industrial_ghysgw' in table_lower:
            return '工业源高盐污水管网表', 'auto_safe'
        if 'industrial_lsf' in table_lower:
            return '工业源硫酸法排污表', 'auto_safe'
        if 'industrial_xzysgw' in table_lower:
            return '工业源现状污水管网表', 'auto_safe'
        if 'industrial_yjf' in table_lower:
            return '工业源有机肥排放表', 'auto_safe'
        if 'industrial_yjsgc' in table_lower:
            return '工业源有机化工工程表', 'auto_safe'
        if 'industrial_ysc' in table_lower:
            return '工业源养殖场表', 'auto_safe'
        if 'outlet_sewage' in table_lower:
            return '排口污水信息表', 'auto_safe'
        if 'boundary_enterprise' in table_lower:
            return '企业边界表', 'auto_safe'
        if 'boundary_park' in table_lower:
            return '园区边界表', 'auto_safe'
        if 'partition_2' in table_lower:
            return '二级分区表', 'auto_safe'
        if 'partition_3' in table_lower:
            return '三级分区表', 'auto_safe'
        if 'watershed' in table_lower:
            return '流域表', 'auto_safe'
        if 'section' in table_lower:
            return '断面信息表', 'auto_safe'
        # _bak 和带中文后缀的表
        if '_bak' in table_lower:
            return '备份表', 'C_hold'
        if '合并' in table_name:
            return '合并表', 'C_hold'

    # 水环境监测表
    if domain == 'water_monitor':
        if 'raster_inversion_config' in table_lower:
            return '遥感反演配置表', 'auto_safe'
        if 'raster_inversion' in table_lower:
            return '遥感反演结果表（合并版）', 'auto_safe'
        if 'raster_info' in table_lower:
            return '遥感影像栅格信息表', 'auto_safe'
        if 'image_info' in table_lower:
            return '遥感影像信息表', 'auto_safe'
        if 'camera_platform' in table_lower:
            return '摄像头云台信息表', 'auto_safe'
        if 'hydrological_info' in table_lower:
            return '水文测站信息表', 'auto_safe'
        if 'meteorological_info' in table_lower:
            return '气象测站信息表', 'auto_safe'
        if 'station_info_v2' in table_lower:
            return '测站信息表（V2）', 'auto_safe'
        if 'station_info' in table_lower:
            return '测站信息表', 'auto_safe'
        if 'uav_info' in table_lower:
            return '无人机信息表', 'auto_safe'
        if 'water_intake' in table_lower:
            return '取水口信息表', 'auto_safe'
        if 'water_source_intake_v2' in table_lower:
            return '水源地取水口信息表（V2）', 'auto_safe'
        if 'water_source_zone_v2' in table_lower:
            return '水源地保护区表（V2）', 'auto_safe'
        if 'water_source_bak' in table_lower:
            return '水源地表（备份）', 'auto_safe'
        if 'water_source' in table_lower:
            return '水源地表', 'auto_safe'
        if 'waterbody_info' in table_lower:
            return '水体基础信息表', 'auto_safe'
        if 'waterquality_day_records' in table_lower:
            return '水质日记录表', 'auto_safe'

    # 气象水文表
    if domain == 'weather_hydro':
        if 'meteorological_predict_day' in table_lower:
            return '气象预测日记录表', 'auto_safe'
        if 'meteorological_predict_hour' in table_lower:
            return '气象预测小时记录表', 'auto_safe'

    # 水溯源表
    if domain == 'water_trace':
        if 'layer_river' in table_lower:
            return '溯源图层河流表', 'auto_safe'
        if 'trace_topology_issue' in table_lower:
            return '溯源拓扑问题记录表', 'auto_safe'
        if 'trace_edge' in table_lower:
            return '溯源拓扑边表', 'auto_safe'
        if 'trace_node' in table_lower:
            return '溯源拓扑节点表', 'auto_safe'
        if 'asset_trace_snap' in table_lower:
            return '资产溯源吸附结果表', 'auto_safe'
        if 'asset_type_dict' in table_lower:
            return '资产类型字典表', 'auto_safe'

    # 遥感表
    if domain == 'remote_sensing':
        if 'industrial_info_yc_bak' in table_lower:
            return '宜昌工业源遥感信息表（备份）', 'C_hold'
        if 'industrial_info_yc' in table_lower:
            return '宜昌工业源遥感信息表', 'auto_safe'
        if 'outlet_info_v2' in table_lower:
            return '排口遥感信息表（V2）', 'auto_safe'
        if 'outlet_live_v2' in table_lower:
            return '排口实时监测表（V2）', 'auto_safe'
        if 'outlet_monitor_v2' in table_lower:
            return '排口监控信息表（V2）', 'auto_safe'
        if 'outlet_remediation_v2' in table_lower:
            return '排口整治信息表（V2）', 'auto_safe'
        if 'outlet_trace_v2' in table_lower:
            return '排口溯源信息表（V2）', 'auto_safe'
        if 'outlet' in table_lower:
            return '排口信息表', 'auto_safe'
        if 'sewage_info_v2' in table_lower:
            return '污水管网信息表（V2）', 'auto_safe'
        if 'sewage_park_info' in table_lower:
            return '园区污水信息表', 'auto_safe'

    # 社会经济表
    if domain == 'social_economic':
        if 'watershed' in table_lower:
            return '社会经济流域统计表', 'auto_safe'

    # 临时表
    if domain == 'staging':
        if 'yichang_river_counts' in table_lower:
            return '宜昌河流导入计数临时表', 'C_hold'
        if 'yichang_river_import' in table_lower:
            return '宜昌河流导入临时表', 'C_hold'
        if 'yichang_river_std' in table_lower:
            return '宜昌河流标准化临时表', 'C_hold'
        if 'sjtysj_cbwrwxtzlxxxt' in table_lower and 'anchorage' in table_lower:
            return '三峡过坝锚地信息临时表', 'C_hold'
        if 'sjtysj_cbwrwxtzlxxxt' in table_lower and 'wharf' in table_lower:
            return '三峡过坝码头信息临时表', 'C_hold'
        if 'sjtysj_cbwrwxtzlxxxt' in table_lower and 'ashore_apply' in table_lower:
            return '三峡过坝靠岸申请临时表', 'C_hold'
        if 'sjtysj_cbwrwxtzlxxxt' in table_lower and 'handover_trans' in table_lower:
            return '三峡过坝交接运输临时表', 'C_hold'
        if 'sjtysj_cbwrwxtzlxxxt' in table_lower and 'receive_ship' in table_lower:
            return '三峡过坝接船评估临时表', 'C_hold'
        if 'sxhyzssj' in table_lower:
            return '三峡航运综合数据临时表', 'C_hold'
        return '临时数据导入表', 'C_hold'

    # PostGIS 系统表
    if domain == 'postgis_system':
        return '空间参考系定义表（PostGIS 系统表）', 'C_hold'

    # 管理后台
    if domain == 'admin_dict':
        return '后台管理字典表', 'auto_safe'

    # 元数据视图
    if domain == 'metadata_view':
        return '元数据配置视图表', 'auto_safe'

    # 质量配置
    if domain == 'quality_setting':
        return '水质评价日质量参数设置表', 'auto_safe'

    return '', 'C_hold'


# ---- 字段注释候选生成 ----
def generate_column_comment(table, col, dtype, domain):
    """生成字段注释候选"""

    # 1) 审计字段 - auto_safe
    if col in AUDIT_FIELDS:
        return AUDIT_FIELDS[col], 'A_auto_safe', 'standard_audit_field', ''

    # 2) ID 字段 - auto_safe
    if col in ID_FIELDS:
        return ID_FIELDS[col], 'A_auto_safe', 'standard_id_field', ''

    # 3) 几何字段 - auto_safe
    if col in GEOM_FIELDS:
        return GEOM_FIELDS[col], 'A_auto_safe', 'standard_geom_field', ''

    # 4) 通用高置信度字段
    if col in COMMON_FIELDS:
        return COMMON_FIELDS[col], 'A_auto_safe', 'standard_common_field', ''

    # 5) 通用中置信度字段
    if col in COMMON_FIELDS_MID:
        return COMMON_FIELDS_MID[col], 'B_review', 'common_field_mid_confidence', '需确认与同表上下文一致'

    # 6) 同表已有注释字段模式推断
    if table in existing_by_table:
        same_table = existing_by_table[table]
        # 同表有类似字段带注释？
        # e.g. layer_inserted/layer_updated → 同表有 statistics 类字段
        pass

    # 7) 特定域规则
    # wm_raster_inversion_config 表
    if table == 'wm_raster_inversion_config':
        cfg_map = {
            'id': ('主键ID', 'A_auto_safe'),
            'type_code': ('反演类型编码', 'B_review'),
            'name': ('配置名称', 'B_review'),
            'boundaries_json': ('分类边界值JSON', 'B_review'),
            'labels_json': ('分类标签JSON', 'B_review'),
            'colors_json': ('分类颜色JSON', 'B_review'),
        }
        if col in cfg_map:
            v, g = cfg_map[col]
            risk = '' if g == 'A_auto_safe' else '需确认JSON字段业务含义'
            return v, g, 'same_table_config_rule', risk

    # gis_ecologicalregion 表
    if table == 'gis_ecologicalregion':
        eco_map = {
            'id': ('主键ID', 'A_auto_safe'),
            'ecological_region_name': ('生态红线区域名称', 'A_auto_safe'),
            'ecological_region_code': ('生态红线区域编码', 'A_auto_safe'),
            'address': ('区域地址', 'A_auto_safe'),
            'geom': ('空间几何数据', 'A_auto_safe'),
            'population': ('区域人口数量', 'B_review'),
            'type': ('生态红线类型', 'B_review'),
            'service_target': ('生态服务目标', 'B_review'),
            'area': ('区域面积', 'A_auto_safe'),
            'ecosystem_vegetation': ('生态系统植被概况', 'B_review'),
            'human_activities': ('人类活动影响描述', 'B_review'),
            'environment_problems': ('生态环境问题描述', 'B_review'),
            'control_measures': ('管控措施描述', 'B_review'),
            'remark': ('备注', 'A_auto_safe'),
        }
        if col in eco_map:
            v, g = eco_map[col]
            risk = '' if g == 'A_auto_safe' else '需确认字段业务含义与生态红线区域相关'
            return v, g, 'domain_gis_ecologicalregion', risk

    # gis_headwaters 表
    if table == 'gis_headwaters':
        hw_map = {
            'id': ('主键ID', 'A_auto_safe'),
            'headwaters_name': ('水源地名称', 'A_auto_safe'),
            'headwaters_code': ('水源地编码', 'A_auto_safe'),
            'address': ('水源地地址', 'A_auto_safe'),
            'geom': ('空间几何数据', 'A_auto_safe'),
            'level': ('水源地级别', 'B_review'),
            'type': ('水源地类型', 'B_review'),
            'water_intake_quantity': ('年取水量', 'B_review'),
            'water_supply_population': ('供水人口数', 'B_review'),
            'is_protect_region': ('是否在保护区范围内', 'B_review'),
            'remark': ('备注', 'A_auto_safe'),
        }
        if col in hw_map:
            v, g = hw_map[col]
            risk = '' if g == 'A_auto_safe' else '需确认与水源地业务含义一致'
            return v, g, 'domain_gis_headwaters', risk

    # gis_naturereserve 表
    if table == 'gis_naturereserve':
        nr_map = {
            'id': ('主键ID', 'A_auto_safe'),
            'nature_reserve_name': ('自然保护区名称', 'A_auto_safe'),
            'nature_reserve_code': ('自然保护区编码', 'A_auto_safe'),
            'address': ('自然保护区地址', 'A_auto_safe'),
            'geom': ('空间几何数据', 'A_auto_safe'),
            'department': ('主管部门', 'B_review'),
            'type': ('自然保护区类型', 'B_review'),
            'level': ('自然保护区级别', 'B_review'),
            'protect_target': ('主要保护对象', 'B_review'),
            'total_area': ('总面积', 'A_auto_safe'),
            'core_area': ('核心区面积', 'A_auto_safe'),
            'buffer_area': ('缓冲区面积', 'A_auto_safe'),
            'manage_org_name': ('管理机构名称', 'B_review'),
            'manage_org_type': ('管理机构类型', 'B_review'),
            'manage_org_level': ('管理机构级别', 'B_review'),
            'population': ('区内人口数量', 'B_review'),
            'first_protect_animals': ('国家一级保护动物', 'B_review'),
            'second_protect_animals': ('国家二级保护动物', 'B_review'),
            'first_protect_plants': ('国家一级保护植物', 'B_review'),
            'second_protect_plants': ('国家二级保护植物', 'B_review'),
        }
        if col in nr_map:
            v, g = nr_map[col]
            risk = '' if g == 'A_auto_safe' else '需确认与自然保护区业务含义一致'
            return v, g, 'domain_gis_naturereserve', risk

    # wm_raster_info / wm_image_info / wm_uav_info / wm_camera_platform / ... id 字段
    if domain == 'water_monitor' and col == 'id':
        return '主键ID', 'A_auto_safe', 'standard_id_field', ''

    # wm_hydrological_info 缺失字段
    if table == 'wm_hydrological_info':
        hydro_map = {
            'region_code': ('行政区划代码', 'A_auto_safe'),
            'geom': ('测站空间位置', 'A_auto_safe'),
            'last_maintenance_time': ('最近维护时间', 'B_review'),
        }
        if col in hydro_map:
            v, g = hydro_map[col]
            risk = '' if g == 'A_auto_safe' else '需确认字段含义'
            return v, g, 'domain_hydrological_info', risk

    # wm_meteorological_info 缺失字段
    if table == 'wm_meteorological_info':
        met_map = {
            'region_code': ('行政区划代码', 'A_auto_safe'),
            'geom': ('测站空间位置', 'A_auto_safe'),
            'last_maintenance_time': ('最近维护时间', 'B_review'),
        }
        if col in met_map:
            v, g = met_map[col]
            risk = '' if g == 'A_auto_safe' else '需确认字段含义'
            return v, g, 'domain_meteorological_info', risk

    # wm_station_info 缺失字段
    if table == 'wm_station_info':
        st_map = {
            'region_code': ('行政区划代码', 'A_auto_safe'),
            'geom': ('测站空间位置', 'A_auto_safe'),
            'last_maintenance_time': ('最近维护时间', 'B_review'),
        }
        if col in st_map:
            v, g = st_map[col]
            risk = '' if g == 'A_auto_safe' else '需确认字段含义'
            return v, g, 'domain_station_info', risk

    # wm_station_info_v2 缺失字段
    if table == 'wm_station_info_v2':
        return AUDIT_FIELDS.get(col, ('', 'C_hold'))[0] or ('', 'C_hold')

    # wm_waterbody_info 缺失字段
    if table == 'wm_waterbody_info':
        wb_map = {
            'water_body_code': ('水体编码', 'A_auto_safe'),
            'water_body_function': ('水体功能类别', 'B_review'),
            'basin': ('所在流域', 'B_review'),
            'country': ('所在国家', 'A_auto_safe'),
            'start_village': ('起点村/社区', 'B_review'),
            'end_village': ('终点村/社区', 'B_review'),
            'up_stream': ('上游水体', 'B_review'),
            'down_stream': ('下游水体', 'B_review'),
            'remark': ('备注', 'A_auto_safe'),
        }
        if col in wb_map:
            v, g = wb_map[col]
            risk = '' if g == 'A_auto_safe' else '需确认与水体信息业务含义一致'
            return v, g, 'domain_waterbody_info', risk

    # wm_water_source / wm_water_source_bak0421 / wm_water_intake
    if table in ('wm_water_source', 'wm_water_source_bak0421'):
        if col == 'id':
            return '主键ID', 'A_auto_safe', 'standard_id_field', ''
        if col == 'geom':
            return '水源地空间范围', 'A_auto_safe', 'standard_geom_field', ''

    if table == 'wm_water_intake':
        if col == 'id':
            return '主键ID', 'A_auto_safe', 'standard_id_field', ''
        if col == 'geom':
            return '取水口空间位置', 'A_auto_safe', 'standard_geom_field', ''

    # wm_water_source_intake_v2 / wm_water_source_zone_v2
    if table in ('wm_water_source_intake_v2', 'wm_water_source_zone_v2'):
        if col == 'id':
            return '主键ID', 'A_auto_safe', 'standard_id_field', ''
        if col in AUDIT_FIELDS:
            return AUDIT_FIELDS[col], 'A_auto_safe', 'standard_audit_field', ''

    # wh_meteorological_predict_day_records / wh_meteorological_predict_hour_records
    if table in ('wh_meteorological_predict_day_records', 'wh_meteorological_predict_hour_records'):
        wx_map = {
            'winddirect_10m_24h': ('10米风向（24小时平均）', 'B_review'),
            'winddirect_10m_1h': ('10米风向（小时）', 'B_review'),
            'winddirect8_10m_24h': ('10米8方位风向（24小时）', 'B_review'),
            'winddirect8_10m_1h': ('10米8方位风向（小时）', 'B_review'),
            'winddirect16_10m_24h': ('10米16方位风向（24小时）', 'B_review'),
            'winddirect16_10m_1h': ('10米16方位风向（小时）', 'B_review'),
            'hum_2m_24h': ('2米湿度（24小时平均）', 'B_review'),
            'hum_2m_24h_min': ('2米湿度最小值（24小时）', 'B_review'),
            'hum_2m_24h_max': ('2米湿度最大值（24小时）', 'B_review'),
            'hum_2m_1h': ('2米湿度（小时）', 'B_review'),
            'stapress_24h': ('地面气压（24小时平均）', 'B_review'),
            'stapress_1h': ('地面气压（小时）', 'B_review'),
            'pressure_24h': ('海平面气压（24小时平均）', 'B_review'),
            'pressure_1h': ('海平面气压（小时）', 'B_review'),
            'p850inver_24h': ('850hPa逆温层高度（24小时）', 'B_review'),
            'p850inver_1h': ('850hPa逆温层高度（小时）', 'B_review'),
            'p925inver_24h': ('925hPa逆温层高度（24小时）', 'B_review'),
            'p925inver_1h': ('925hPa逆温层高度（小时）', 'B_review'),
            'swdown_24h': ('短波辐射通量（24小时平均）', 'B_review'),
            'swdown_1h': ('短波辐射通量（小时）', 'B_review'),
            'glw_24h': ('长波辐射通量（24小时平均）', 'B_review'),
            'glw_1h': ('长波辐射通量（小时）', 'B_review'),
            'height_24h': ('边界层高度（24小时）', 'B_review'),
            'height_1h': ('边界层高度（小时）', 'B_review'),
            'rain_24h_total': ('24小时总降雨量', 'B_review'),
            'rain_1h': ('小时降雨量', 'B_review'),
            'rain_3h': ('3小时累计降雨量', 'B_review'),
            'rain_6h': ('6小时累计降雨量', 'B_review'),
            'rain_12h': ('12小时累计降雨量', 'B_review'),
            'rain_24h': ('24小时累计降雨量', 'B_review'),
            'dewpoint_24h': ('露点温度（24小时）', 'B_review'),
            'dewpoint_1h': ('露点温度（小时）', 'B_review'),
            'lowcloud_24h': ('低云量（24小时）', 'B_review'),
            'lowcloud_1h': ('低云量（小时）', 'B_review'),
            'midcloud_24h': ('中云量（24小时）', 'B_review'),
            'midcloud_1h': ('中云量（小时）', 'B_review'),
            'highcloud_24h': ('高云量（24小时）', 'B_review'),
            'highcloud_1h': ('高云量（小时）', 'B_review'),
            'totalcloud_24h': ('总云量（24小时）', 'B_review'),
            'totalcloud_1h': ('总云量（小时）', 'B_review'),
            'tem_2m_24h': ('2米温度（24小时平均）', 'B_review'),
            'tem_2m_24h_min': ('2米温度最小值（24小时）', 'B_review'),
            'tem_2m_24h_max': ('2米温度最大值（24小时）', 'B_review'),
            'tem_2m_1h': ('2米温度（小时）', 'B_review'),
            'visib_24h': ('能见度（24小时）', 'B_review'),
            'visib_1h': ('能见度（小时）', 'B_review'),
            'pbl_24h': ('行星边界层高度（24小时平均）', 'B_review'),
            'pbl_24h_min': ('行星边界层高度最小值（24小时）', 'B_review'),
            'pbl_24h_max': ('行星边界层高度最大值（24小时）', 'B_review'),
            'pbl_1h': ('行星边界层高度（小时）', 'B_review'),
            'windspeed_10m_24h': ('10米风速（24小时平均）', 'B_review'),
            'windspeed_10m_24h_min': ('10米风速最小值（24小时）', 'B_review'),
            'windspeed_10m_24h_max': ('10米风速最大值（24小时）', 'B_review'),
            'windspeed_10m_1h': ('10米风速（小时）', 'B_review'),
            'dtem_2m_1h': ('2米温度1小时变化', 'B_review'),
            'dtem_2m_3h': ('2米温度3小时变化', 'B_review'),
            'dtem_2m_6h': ('2米温度6小时变化', 'B_review'),
            'dtem_2m_12h': ('2米温度12小时变化', 'B_review'),
            'dtem_2m_24h': ('2米温度24小时变化', 'B_review'),
            'predictiontime': ('预测时间', 'A_auto_safe'),
            'predictioninterval': ('预测间隔（小时）', 'A_auto_safe'),
            'datadate': ('数据日期', 'A_auto_safe'),
        }
        if col in wx_map:
            v, g = wx_map[col]
            risk = '' if g == 'A_auto_safe' else '基于字段名推断，需气象业务方确认'
            return v, g, 'domain_weather_predict', risk

    # waterquality_day_records
    if table == 'wm_waterquality_day_records':
        wq_map = {
            'status': ('记录状态', 'B_review'),
            'record_type': ('记录类型', 'B_review'),
        }
        if col in wq_map:
            v, g = wq_map[col]
            return v, g, 'domain_waterquality', '需确认枚举值含义'

    # wst_ 系列
    if table == 'wst_layer_river':
        wlr_map = {
            'id': ('主键ID', 'A_auto_safe'),
            'river_code': ('河流编码', 'A_auto_safe'),
            'river_name': ('河流名称', 'A_auto_safe'),
            'next_down': ('下游河流ID', 'B_review'),
            'river_class': ('河流类别', 'B_review'),
            'length_km': ('河流长度（公里）', 'B_review'),
            'from_z': ('起点高程', 'B_review'),
            'to_z': ('终点高程', 'B_review'),
            'geom': ('河流空间线段', 'A_auto_safe'),
            'metadata_json': ('元数据JSON', 'B_review'),
        }
        if col in wlr_map:
            v, g = wlr_map[col]
            risk = '' if g == 'A_auto_safe' else '需确认与溯源图层河流含义一致'
            return v, g, 'domain_wst_layer_river', risk

    if table == 'wst_trace_topology_issue':
        tti_map = {
            'id': ('主键ID', 'A_auto_safe'),
            'issue_type': ('问题类型', 'B_review'),
            'issue_name': ('问题名称', 'B_review'),
            'issue_level': ('问题级别', 'B_review'),
            'object_type': ('关联对象类型', 'B_review'),
            'object_id': ('关联对象ID', 'B_review'),
            'object_name': ('关联对象名称', 'B_review'),
            'status': ('问题状态', 'B_review'),
            'geom': ('问题空间位置', 'A_auto_safe'),
            'issue_desc': ('问题详细描述', 'B_review'),
            'metadata_json': ('元数据JSON', 'B_review'),
            'remark': ('备注', 'A_auto_safe'),
            'del_flag': ('删除标志：0-正常，1-已删除', 'A_auto_safe'),
        }
        if col in tti_map:
            v, g = tti_map[col]
            risk = '' if g == 'A_auto_safe' else '需确认与溯源拓扑问题含义一致'
            return v, g, 'domain_wst_topology_issue', risk

    if table == 'wst_trace_edge':
        te_map = {
            'source_asset_id': ('原始资产ID', 'B_review'),
            'from_node_id': ('起始节点ID', 'B_review'),
            'to_node_id': ('终止节点ID', 'B_review'),
            'direction_status': ('流向状态', 'B_review'),
        }
        if col in te_map:
            v, g = te_map[col]
            risk = '' if g == 'A_auto_safe' else '需确认与溯源边拓扑含义一致'
            return v, g, 'domain_wst_trace_edge', risk

    if table == 'wst_trace_node':
        tn_map = {
            'asset_id': ('关联资产ID', 'B_review'),
        }
        if col in tn_map:
            v, g = tn_map[col]
            return v, g, 'domain_wst_trace_node', '需确认资产ID来源'

    if table == 'wst_asset_trace_snap':
        snap_map = {
            'snap_node_id': ('吸附节点ID', 'B_review'),
            'snap_edge_id': ('吸附边ID', 'B_review'),
            'snap_distance_m': ('吸附距离（米）', 'B_review'),
            'status': ('吸附状态', 'B_review'),
        }
        if col in snap_map:
            v, g = snap_map[col]
            risk = '' if g == 'A_auto_safe' else '需确认与吸附结果含义一致'
            return v, g, 'domain_wst_snap', risk

    if table == 'wst_asset_type_dict':
        atd_map = {
            'asset_group': ('资产分组编码', 'B_review'),
            'asset_group_name': ('资产分组名称', 'B_review'),
            'group_sort': ('分组排序号', 'B_review'),
            'group_description': ('分组描述', 'B_review'),
        }
        if col in atd_map:
            v, g = atd_map[col]
            return v, g, 'domain_wst_asset_type', '需确认分组含义'

    # _stg_yichang_river_counts
    if table == '_stg_yichang_river_counts':
        yc_map = {
            'layer_inserted': ('图层插入计数', 'C_hold'),
            'layer_updated': ('图层更新计数', 'C_hold'),
            'asset_inserted': ('资产插入计数', 'C_hold'),
            'asset_updated': ('资产更新计数', 'C_hold'),
            'skipped': ('跳过计数', 'C_hold'),
        }
        if col in yc_map:
            v, g = yc_map[col]
            return v, g, 'domain_staging_counts', '临时统计表，注释基于字段名推断，业务方确认后补齐'

    # _stg_yichang_river_import
    if table == '_stg_yichang_river_import':
        yri_map = {
            'gid': ('地理要素唯一标识', 'B_review'),
            'OBJECTID': ('对象唯一标识', 'B_review'),
            'Nextdown': ('下游河流ID', 'B_review'),
            'MAINRIVID': ('干流ID', 'B_review'),
            'Hydrocount': ('水文计数', 'B_review'),
            'Rclass': ('河流类别编码', 'B_review'),
            'Rlenth': ('河流长度', 'B_review'),
            'Hydrolenth': ('水文计算长度', 'B_review'),
            'Rcatch': ('汇水面积', 'B_review'),
            'TCatch': ('总汇水面积', 'B_review'),
            'Rname': ('河流名称', 'B_review'),
            'Shape_Leng': ('要素长度', 'B_review'),
            'RiverID': ('河流ID', 'B_review'),
            'RclassDISP': ('河流类别显示编码', 'B_review'),
            'OSMratio': ('OSM匹配比例', 'B_review'),
            'GRITratio': ('GRIT匹配比例', 'B_review'),
            'Hydroratio': ('水文匹配比例', 'B_review'),
            'NameList': ('河流名称列表', 'B_review'),
            'OrignCNT': ('原始数据来源', 'B_review'),
            'SEG_ID': ('分段ID', 'B_review'),
            'LEN': ('分段长度', 'B_review'),
            'FLIPPED': ('流向是否翻转', 'B_review'),
            'FROM_Z': ('起点高程', 'B_review'),
            'TO_Z': ('终点高程', 'B_review'),
            'STR_ORD': ('Strahler河流分级', 'B_review'),
            'SHR_ORD': ('Shreve河流分级', 'B_review'),
            'geom': ('河流空间线段', 'A_auto_safe'),
        }
        if col in yri_map:
            v, g = yri_map[col]
            risk = '' if g == 'A_auto_safe' else '临时导入表，基于原始字段名推断，建议确认'
            return v, g, 'domain_staging_river_import', risk

    # _stg_yichang_river_std
    if table == '_stg_yichang_river_std':
        yrs_map = {
            'gid': ('地理要素唯一标识', 'B_review'),
            'river_code': ('河流编码', 'A_auto_safe'),
            'river_name': ('河流名称', 'A_auto_safe'),
            'next_down': ('下游河流ID', 'B_review'),
            'river_class': ('河流类别', 'B_review'),
            'length_km': ('河流长度（公里）', 'B_review'),
            'from_z': ('起点高程', 'B_review'),
            'to_z': ('终点高程', 'B_review'),
            'geom': ('河流空间线段', 'A_auto_safe'),
            'metadata_json': ('元数据JSON', 'B_review'),
        }
        if col in yrs_map:
            v, g = yrs_map[col]
            risk = '' if g == 'A_auto_safe' else '标准化表，基于同名字段推断'
            return v, g, 'domain_staging_river_std', risk

    # gis_region
    if table == 'gis_region':
        gr_map = {
            'region_code': ('行政区划编码', 'A_auto_safe'),
            'region_name': ('行政区划名称', 'A_auto_safe'),
            'control_unit_id': ('所属管控单元ID', 'B_review'),
            'region_level': ('区划级别', 'B_review'),
            'parent_code': ('父级区划编码', 'B_review'),
            'code': ('编码', 'A_auto_safe'),
            'address': ('地址', 'A_auto_safe'),
            'remark': ('备注', 'A_auto_safe'),
        }
        if col in gr_map:
            v, g = gr_map[col]
            risk = '' if g == 'A_auto_safe' else '需确认与行政区划业务逻辑一致'
            return v, g, 'domain_gis_region', risk

    # gis_region_city / gis_region_county / gis_region_township
    if table in ('gis_region_city', 'gis_region_county', 'gis_region_township'):
        if col == 'id':
            return '主键ID', 'A_auto_safe', 'standard_id_field', ''
        if col == 'geom':
            return '区划空间范围', 'A_auto_safe', 'standard_geom_field', ''

    # gis_region_population
    if table == 'gis_region_population':
        rp_map = {
            'id': ('主键ID', 'A_auto_safe'),
            'region_id': ('行政区划ID', 'B_review'),
            'city_population': ('城镇人口', 'B_review'),
            'city_area': ('城镇面积', 'B_review'),
            'city_quantity': ('城镇数量', 'B_review'),
            'rural_population': ('农村人口', 'B_review'),
            'rural_area': ('农村面积', 'B_review'),
            'rural_quantity': ('农村数量', 'B_review'),
            'year': ('统计年份', 'A_auto_safe'),
        }
        if col in rp_map:
            v, g = rp_map[col]
            risk = '' if g == 'A_auto_safe' else '需确认人口统计数据口径'
            return v, g, 'domain_region_population', risk

    # gis_watershed_partition
    if table == 'gis_watershed_partition':
        if col == 'id':
            return '主键ID', 'A_auto_safe', 'standard_id_field', ''

    # gis_watershed_partition_3/4
    if table in ('gis_watershed_partition_3', 'gis_watershed_partition_4'):
        if col == 'id':
            return '主键ID', 'A_auto_safe', 'standard_id_field', ''
        if col == 'geom':
            return '流域分区空间范围', 'A_auto_safe', 'standard_geom_field', ''
        if col == 'poly_area':
            return '分区面积', 'B_review', 'common_field_mid_confidence', '需确认面积单位'
        if col.isdigit():
            return f'{col}年数据', 'C_hold', 'digit_column_name', '年份命名字段，需业务方确认具体含义'

    # gis_control_unit
    if table == 'gis_control_unit':
        return '', 'C_hold', 'needs_manual', '证据不足，建议人工填写'

    # gis_poi
    if table == 'gis_poi':
        return AUDIT_FIELDS.get(col, ('', 'C_hold'))

    # metadata_view
    if table == 'metadata_view':
        md_map = {
            'code': ('元数据编码', 'B_review'),
            'parent_id': ('父级元数据ID', 'B_review'),
            'aliasname': ('元数据别名', 'B_review'),
            'type': ('元数据类型', 'B_review'),
            'LayerName': ('对应的GIS图层名称', 'B_review'),
            'LayerType': ('对应的GIS图层类型', 'B_review'),
        }
        if col in md_map:
            v, g = md_map[col]
            return v, g, 'domain_metadata_view', '需确认元数据配置具体用途'

    # ad_dict
    if table == 'ad_dict':
        return AUDIT_FIELDS.get(col, ('', 'C_hold'))

    # day_quality_setting
    if table == 'day_quality_setting':
        dq_map = {
            'span_value': ('水质变化幅值', 'B_review'),
            'zero_standard_value': ('零标准值', 'C_hold'),
            'span_standard_value': ('标准幅值', 'C_hold'),
        }
        if col in dq_map:
            v, g = dq_map[col]
            risk = '基于字段名推断，需水质评价业务方确认'
            return v, g, 'domain_quality_setting', risk

    # layer_reservoir_provincial / layer_river_provincial / layer_reservoir_provincial_label
    # These have MANY columns matching COMMON_FIELDS_MID already covered above
    # But let's handle specific ones not covered

    # layer_boundary_enterprise / layer_boundary_park
    if table in ('layer_boundary_enterprise', 'layer_boundary_park'):
        if col == 'id':
            return '主键ID', 'A_auto_safe', 'standard_id_field', ''
        if col == 'name':
            return '名称', 'A_auto_safe', 'standard_common_field', ''
        if col == 'code':
            return '编码', 'A_auto_safe', 'standard_common_field', ''
        if col == 'geom':
            return '边界空间范围', 'A_auto_safe', 'standard_geom_field', ''

    # layer_industrial_*
    if table.startswith('layer_industrial_'):
        if col == 'id':
            return '主键ID', 'A_auto_safe', 'standard_id_field', ''
        if col == 'geom':
            return '空间几何数据', 'A_auto_safe', 'standard_geom_field', ''
        if col == 'name':
            return '工业源名称', 'B_review', 'domain_industrial', ''
        if col == 'code':
            return '工业源编码', 'B_review', 'domain_industrial', ''
        if col == 'x':
            return 'X坐标', 'A_auto_safe', 'standard_common_field', ''
        if col == 'y':
            return 'Y坐标', 'A_auto_safe', 'standard_common_field', ''

    # layer_outlet_sewage
    if table == 'layer_outlet_sewage':
        if col in ('id', 'x', 'y', 'name', 'code'):
            return COMMON_FIELDS.get(col, ID_FIELDS.get(col, '')), 'A_auto_safe', 'standard_common_field', ''
        if col == 'geom':
            return '排口空间位置', 'A_auto_safe', 'standard_geom_field', ''

    # layer_partition_2 / layer_partition_3
    if table in ('layer_partition_2', 'layer_partition_3'):
        if col == 'id':
            return '主键ID', 'A_auto_safe', 'standard_id_field', ''
        if col == 'geom':
            return '分区空间范围', 'A_auto_safe', 'standard_geom_field', ''

    # layer_watershed
    if table == 'layer_watershed':
        if col == 'id':
            return '主键ID', 'A_auto_safe', 'standard_id_field', ''
        if col == 'name':
            return '流域名称', 'B_review', 'domain_watershed', ''
        if col == 'code':
            return '流域编码', 'B_review', 'domain_watershed', ''
        if col == 'geom':
            return '流域空间线段', 'A_auto_safe', 'standard_geom_field', ''

    # layer_section
    if table == 'layer_section':
        if col in ('id', 'x', 'y', 'name', 'code'):
            return COMMON_FIELDS.get(col, ID_FIELDS.get(col, '')), 'A_auto_safe', 'standard_common_field', ''
        if col == 'geom':
            return '断面空间位置', 'A_auto_safe', 'standard_geom_field', ''

    # rs_* 表
    if table == 'rs_industrial_info_yc':
        return AUDIT_FIELDS.get(col, ('', 'C_hold'))
    if table == 'rs_outlet':
        if col == 'quick_detect_desc':
            return '快速检测描述', 'B_review', 'domain_rs_outlet', '需确认字段含义'

    if table in ('rs_outlet_info_v2', 'rs_outlet_live_v2', 'rs_outlet_monitor_v2',
                 'rs_outlet_remediation_v2', 'rs_outlet_trace_v2'):
        if col == 'id':
            return '主键ID', 'A_auto_safe', 'standard_id_field', ''
        if col in AUDIT_FIELDS:
            return AUDIT_FIELDS[col], 'A_auto_safe', 'standard_audit_field', ''

    if table == 'rs_sewage_info_v2':
        if col == 'id':
            return '主键ID', 'A_auto_safe', 'standard_id_field', ''
        if col in AUDIT_FIELDS:
            return AUDIT_FIELDS[col], 'A_auto_safe', 'standard_audit_field', ''

    if table == 'rs_sewage_park_info':
        if col in AUDIT_FIELDS:
            return AUDIT_FIELDS[col], 'A_auto_safe', 'standard_audit_field', ''

    # se_watershed
    if table == 'se_watershed':
        if col == 'id':
            return '主键ID', 'A_auto_safe', 'standard_id_field', ''

    # spatial_ref_sys
    if table == 'spatial_ref_sys':
        srs_map = {
            'srid': ('空间参考标识符', 'A_auto_safe'),
            'auth_name': ('空间参考系授权机构名称', 'A_auto_safe'),
            'auth_srid': ('空间参考系授权机构SRID', 'A_auto_safe'),
            'srtext': ('空间参考系WKT描述', 'A_auto_safe'),
            'proj4text': ('空间参考系Proj4描述', 'A_auto_safe'),
        }
        if col in srs_map:
            return srs_map[col], 'A_auto_safe', 'postgis_system_table', 'PostGIS 系统表，注释固定'

    # stg_ycsjtysj_sxhyzssj_base_ship_df
    if 'sxhyzssj' in table.lower() and 'base_ship' in table.lower():
        ship_map = {
            'mmsi': ('海上移动通信业务标识（MMSI）', 'B_review'),
        }
        if col in ship_map:
            return ship_map[col], 'B_review', 'domain_staging_ship', '需航运业务方确认'
        if col in AUDIT_FIELDS:
            return AUDIT_FIELDS[col], 'A_auto_safe', 'standard_audit_field', ''

    # stg_* 临时表通用审计字段
    if domain == 'staging':
        if col in AUDIT_FIELDS:
            return AUDIT_FIELDS[col], 'A_auto_safe', 'standard_audit_field', ''
        # 特殊字段
        staging_special = {
            'shlj_text': ('生活垃圾处理文本描述', 'C_hold'),
            'fy_time': ('反应时间', 'C_hold'),
            'hyws_time': ('行业卫生审批时间', 'C_hold'),
            'shws_time': ('社会卫生审批时间', 'C_hold'),
            'from_port_province': ('起始港口省份', 'C_hold'),
            'from_port_city': ('起始港口城市', 'C_hold'),
            'to_port_province': ('目的港口省份', 'C_hold'),
            'to_port_city': ('目的港口城市', 'C_hold'),
            'trans_no': ('运输编号', 'C_hold'),
            'js_apply_no': ('接收申请编号', 'C_hold'),
            'js_detail_id': ('接收明细ID', 'C_hold'),
        }
        if col in staging_special:
            v, g = staging_special[col]
            return v, g, 'staging_unknown', '临时表数据，基于字段名推断，建议人工确认'

    # _bak / backup tables
    if '_bak' in table.lower() or 'bak' in table.lower():
        if col in AUDIT_FIELDS:
            return AUDIT_FIELDS[col], 'A_auto_safe', 'standard_audit_field', ''
        # Fall through to generic handling
        if col in COMMON_FIELDS:
            return COMMON_FIELDS[col], 'A_auto_safe', 'standard_common_field', ''
        if col in COMMON_FIELDS_MID:
            return COMMON_FIELDS_MID[col], 'B_review', 'common_field_mid_confidence', '需确认与主表一致'

    # 8) 最终 fallback：基于字段名的启发式推断
    col_lower = col.lower()

    # 字段名包含明显语义
    if 'name' in col_lower and 'json' not in col_lower and '_name' in col_lower:
        prefix = col.replace('_name', '')
        return f'{prefix}名称', 'B_review', 'heuristic_suffix_name', '基于字段名后缀 _name 推断'

    if col_lower.endswith('_code') or col_lower.endswith('_id'):
        prefix = col_lower.replace('_code', '').replace('_id', '')
        prefix = prefix.replace('_', ' ')
        return f'{prefix}编码', 'B_review', 'heuristic_suffix_code', '基于字段名后缀推断，需确认业务含义'

    if col_lower.endswith('_time') or col_lower.endswith('_date'):
        return '时间戳', 'B_review', 'heuristic_suffix_time', '基于字段名后缀 _time/_date 推断'

    if col_lower.endswith('_json'):
        prefix = col_lower.replace('_json', '').replace('_', ' ')
        return f'{prefix}（JSON格式）', 'B_review', 'heuristic_suffix_json', 'JSON字段，需确认存储内容'

    if col_lower.endswith('_desc') or col_lower.endswith('_description'):
        return '描述文本', 'B_review', 'heuristic_suffix_desc', '基于字段名后缀推断'

    # 无法推断
    return '', 'C_hold', 'needs_manual', '缺乏足够上下文，建议人工填写'


# ---- 主流程 ----
def main():
    print("=== 全库缺注释候选生成 V2 ===\n")

    # --- 字段注释候选 ---
    field_rows = []
    grade_counts = defaultdict(int)

    for parts in missing_cols:
        schema, table, col, dtype = parts[0], parts[1], parts[2], parts[3]
        domain = classify_table(table)

        candidate, grade, source, risk_reason = generate_column_comment(table, col, dtype, domain)

        # 补充 sample_hint
        sample_hint = ''
        if grade == 'B_review' and not risk_reason:
            risk_reason = '基于字段名和表域规则推断，建议人工快速确认'

        field_rows.append({
            'schema_name': schema,
            'table_name': table,
            'column_name': col,
            'data_type': dtype,
            'current_comment': '',
            'candidate_comment': candidate,
            'confidence': 'high' if grade == 'A_auto_safe' else ('medium' if grade == 'B_review' else 'low'),
            'grade': grade,
            'evidence': f'表域: {domain}' + (f'; 来源: {source}' if source else ''),
            'source_rule': source,
            'sample_hint': sample_hint,
            'risk_reason': risk_reason,
        })
        grade_counts[grade] += 1

    # 表注释候选（统一 grade 大小写）
    def normalize_grade(g):
        if g in ('auto_safe', 'A_auto_safe'):
            return 'A_auto_safe'
        if g in ('B_review',):
            return 'B_review'
        return 'C_hold'

    # --- 表注释候选 ---
    table_rows = []
    table_grade_counts = defaultdict(int)

    for parts in missing_tables:
        schema, table = parts[0], parts[1]
        domain = classify_table(table)

        candidate, grade = generate_table_comment(table, domain)
        grade = normalize_grade(grade)
        if grade == 'A_auto_safe':
            confidence = 'high'
        elif grade == 'B_review':
            confidence = 'medium'
        else:
            confidence = 'low'

        source = f'表域: {domain}; 表名规则推断'
        risk_reason = ''
        if grade == 'C_hold':
            risk_reason = '信息不足或为系统/临时表，建议人工判断'

        table_rows.append({
            'schema_name': schema,
            'table_name': table,
            'current_table_comment': '',
            'candidate_table_comment': candidate,
            'confidence': confidence,
            'grade': grade,
            'evidence': f'表域: {domain}',
            'source_rule': source,
            'risk_reason': risk_reason,
        })
        table_grade_counts[grade] += 1

    # ---- 写入 CSV ----
    field_cols = ['schema_name', 'table_name', 'column_name', 'data_type', 'current_comment',
                  'candidate_comment', 'confidence', 'grade', 'evidence', 'source_rule',
                  'sample_hint', 'risk_reason']

    def write_csv(filename, rows, cols):
        path = os.path.join(OUT_DIR, filename)
        with open(path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=cols, lineterminator='\n')
            writer.writeheader()
            writer.writerows(rows)
        print(f"  写入: {filename} ({len(rows)} 行)")
        return path

    write_csv('missing_comment_candidates_v2.csv', field_rows, field_cols)

    table_cols = ['schema_name', 'table_name', 'current_table_comment', 'candidate_table_comment',
                  'confidence', 'grade', 'evidence', 'source_rule', 'risk_reason']
    write_csv('missing_table_comment_candidates_v2.csv', table_rows, table_cols)

    # 按分级拆分
    auto_safe = [r for r in field_rows if r['grade'] == 'A_auto_safe']
    review = [r for r in field_rows if r['grade'] == 'B_review']
    hold = [r for r in field_rows if r['grade'] == 'C_hold']

    write_csv('auto_safe_candidates_v2.csv', auto_safe,
              field_cols)

    # review_needed: 字段 B_review
    write_csv('review_needed_candidates_v2.csv', review, field_cols)

    # hold: 字段 C_hold
    write_csv('hold_candidates_v2.csv', hold, field_cols)

    # ---- 输出统计 ----
    print(f"\n=== 统计 ===")
    print(f"  缺字段注释总数:      {len(field_rows)}")
    print(f"  缺表注释总数:        {len(table_rows)}")
    print(f"  A_auto_safe (字段):  {grade_counts['A_auto_safe']}")
    print(f"  A_auto_safe (表):    {table_grade_counts['A_auto_safe']}")
    print(f"  B_review (字段):     {grade_counts['B_review']}")
    print(f"  B_review (表):       {table_grade_counts['B_review']}")
    print(f"  C_hold (字段):       {grade_counts['C_hold']}")
    print(f"  C_hold (表):         {table_grade_counts['C_hold']}")

    # ---- 写汇总 MD ----
    summary_path = os.path.join(OUT_DIR, 'metadata_completion_batch_v2_summary.md')
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write(f"""# 全库缺注释候选生成 V2 — 汇总报告

**生成时间**: 2026-07-08
**状态**: 候选已生成，未执行 COMMENT ON，未训练 Vanna

---

## 一、扫描范围

| 项目 | 值 |
|------|-----|
| Schema | public |
| 数据库 | gt_monitor (local-timescale) |
| 总表数（含已有注释表） | public schema 所有普通表 |

---

## 二、扫描结果

| 指标 | 数量 |
|------|------|
| 缺字段注释 | {len(field_rows)} |
| 缺表注释 | {len(table_rows)} |

---

## 三、分级统计

| 分级 | 说明 | 字段数 | 表数 |
|------|------|--------|------|
| A_auto_safe | 高置信度，可批量补 | {grade_counts['A_auto_safe']} | {table_grade_counts['A_auto_safe']} |
| B_review | 有候选，需人工快速确认 | {grade_counts['B_review']} | {table_grade_counts['B_review']} |
| C_hold | 证据不足，暂缓 | {grade_counts['C_hold']} | {table_grade_counts['C_hold']} |
| **合计** | | **{len(field_rows)}** | **{len(table_rows)}** |

---

## 四、A_auto_safe 候选说明

主要来源：

1. **标准审计字段**：create_by / create_time / update_by / update_time / del_flag — 跨所有表
2. **标准 ID 字段**：id / gid / objectid / region_id 等
3. **几何字段**：geom
4. **通用高频字段**：name / code / type / address / remark 等
5. **表域规则高置信**：如 gis_ecologicalregion 的表名语义确定性很高

---

## 五、B_review 候选说明

需要人工确认的场景：

1. **气象预测字段**：基于字段名缩写推断物理量含义，需气象业务方确认
2. **特定业务字段**：如自然保护区特有字段、水源地特有字段等，注释基于表名语义推断
3. **临时导入表**：基于原始字段名推断，业务方确认后可直接升级为 A
4. **JSON / JSONB 字段**：推断可能包含的内容类型

---

## 六、C_hold 候选说明

暂缓的场景：

1. **系统表**（如 spatial_ref_sys — PostGIS 内置表）
2. **备份表**（_bak 后缀，注释应与主表同步）
3. **临时表**（_stg 前缀，字段名简写难以推断）
4. **年份命名字段**（如 2021, 2025, 2035）
5. **信息严重不足**的字段

---

## 七、生成文件清单

| 文件 | 内容 |
|------|------|
| `missing_comment_candidates_v2.csv` | 全量缺字段注释候选（{len(field_rows)} 行） |
| `missing_table_comment_candidates_v2.csv` | 全量缺表注释候选（{len(table_rows)} 行） |
| `auto_safe_candidates_v2.csv` | A_auto_safe 候选（{(grade_counts['A_auto_safe'] + table_grade_counts['A_auto_safe'])} 行） |
| `review_needed_candidates_v2.csv` | B_review 候选（{(grade_counts['B_review'] + table_grade_counts['B_review'])} 行） |
| `hold_candidates_v2.csv` | C_hold 候选（{(grade_counts['C_hold'] + table_grade_counts['C_hold'])} 行） |
| `metadata_completion_batch_v2_summary.md` | 本汇总报告 |
| `generate_metadata_completion_candidates_v2.py` | 生成脚本 |

---

## 八、阶段边界声明

> - ❌ 未执行 COMMENT ON
> - ❌ 未修改数据库
> - ❌ 未训练 Vanna
> - ❌ 未写入 vanna_data / agent_data
> - ❌ 未修改已有注释
> - ❌ 未修改项目代码
""")
    print(f"  写入: metadata_completion_batch_v2_summary.md")

    # 脚本已在输出目录，无需复制
    print(f"  脚本: generate_metadata_completion_candidates_v2.py (已在输出目录)")

    print("\n=== 完成 ===")
    return grade_counts, table_grade_counts


if __name__ == "__main__":
    main()
