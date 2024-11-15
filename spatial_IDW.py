'''
README：
    本次操作用到的数据坐标投影为WGS-1984
    已知点文件：CA_cities_wgs1984.shp
    待插值点文件：point_wgs1984.shp
    利用ArcMap提前生成待插值点文件，在使用时请按照对应关系进行替换
'''

import geopandas as gpd
import pandas as pd
import tqdm, time, math
import plotly.graph_objects as go

class OzoneModel3D:
    def __init__(self, known_file, unknown_file):
        """
        Args:
            known_file (str): 已知数据的文件名。
            unknown_file (str): 未知数据的文件名。

        Attributes:
            known_file (str): 已知数据的文件名。
            unknown_file (str): 未知数据的文件名。
            known (Any, optional): 已知数据的解析结果，默认为None。
            unknown (Any, optional): 未知数据的解析结果，默认为None。
            known_lats (list): 已知数据的纬度列表，默认为空列表。
            known_lons (list): 已知数据的经度列表，默认为空列表。
            unknown_lats (list): 未知数据的纬度列表，默认为空列表。
            unknown_lons (list): 未知数据的经度列表，默认为空列表。
            ozone_weight (list): 臭氧权重列表，默认为空列表。
        """
        self.known_file = known_file
        self.unknown_file = unknown_file
        self.known = None
        self.unknown = None
        self.known_lats = []
        self.known_lons = []
        self.unknown_lats = []
        self.unknown_lons = []
        self.ozone_weight = []

    # 将读取过程、计算过程转化为进度条，完成可视化
    def simulate_reading_delay(self, chunk_size=10):
        time.sleep(chunk_size * 0.01)

    # 读取文件数据
    def read_file_with_progress(self, file_path):
        total_chunks = 10
        for i in tqdm.tqdm(range(total_chunks), desc="Reading file", unit="chunk"):
            self.simulate_reading_delay()
        gdf = gpd.read_file(file_path)
        return gdf

    # haversine:将经纬度转化为实地距离(km)
    def haversine(self, lon1, lat1, lon2, lat2):
        lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.asin(math.sqrt(a))
        r = 6371.0
        distance = c * r
        return distance

    class pointsExtractor:
        # 读取地理信息
        def __init__(self, geodataframe):
            self.geodataframe = geodataframe
        # 读取经纬度坐标
        def known_x_y(self):
            lats = []
            lons = []
            for point in self.geodataframe.geometry:
                lats.append(point.y)
                lons.append(point.x)
            return lats, lons

    def load_data(self):
        self.known = self.read_file_with_progress(self.known_file)
        self.unknown = self.read_file_with_progress(self.unknown_file)

        # OZONE: 目标值
        self.knownData = self.known['OZONE']

        # 获取已知点坐标
        known_points_extractor = self.pointsExtractor(self.known)
        unknown_points_extractor = self.pointsExtractor(self.unknown)
        self.known_lats, self.known_lons = known_points_extractor.known_x_y()
        self.unknown_lats, self.unknown_lons = unknown_points_extractor.known_x_y()
        print(f'已知点坐标共读取{len(self.known_lats)}个\n未知点坐标共读取{len(self.unknown_lats)}个')

    # IDW的核心计算步骤
    def compute_ozone_weights(self, p):
        self.ozone_weight = []
        print("计算权重中...")
        for j in tqdm.tqdm(range(len(self.unknown_lats)), desc="Processing points", unit="point"):
            ozone_sum = 0
            weight_sum = 0
            for k in range(len(self.known_lats)):
                distance = self.haversine(self.known_lons[k], self.known_lats[k], self.unknown_lons[j],
                                          self.unknown_lats[j])
                if distance == 0:
                    continue
                weight = 1 / distance ** p
                weight_sum += weight
                ozone_sum += weight * self.knownData[k]
            if weight_sum > 0:
                self.ozone_weight.append(ozone_sum / weight_sum)
            else:
                self.ozone_weight.append(float('0'))
    # 保存成生成的文件
    def save_to_excel(self, filename):
        df = pd.DataFrame({'OZONE': self.ozone_weight})
        df.to_excel(filename, sheet_name='sheet0', index=True)
        print(f'已完成数据导出，请参看文件夹中的"{filename}"')

    # 数据可视化，转化为3D模型
    def plot_3d_model(self):
        fig = go.Figure(data=[go.Mesh3d(
            x=self.unknown_lons,
            y=self.unknown_lats,
            z=self.ozone_weight,
            opacity=0.5,
            colorscale='Viridis',
            intensity=self.ozone_weight,
            colorbar=dict(title='Ozone')
        )])
        print('正在制作3D模型')
        fig.update_layout(
            scene=dict(
                xaxis_title='经度',
                yaxis_title='纬度',
                zaxis_title='臭氧值'
            ),
            title="IDW下臭氧浓度随经纬度的变化"
        )
        fig.show()

    def run(self, p, excel_filename='IDW_OZONE.xlsx'):
        self.load_data()
        self.compute_ozone_weights(p)
        self.save_to_excel(excel_filename)
        self.plot_3d_model()

if __name__ == '__main__':
    model = OzoneModel3D('spatial/CA_cities_wgs1984.shp', 'spatial/point_wgs1984.shp')
    p = int(input('请输入幂的值：'))
    model.run(p, 'IDW_OZONE.xlsx')

