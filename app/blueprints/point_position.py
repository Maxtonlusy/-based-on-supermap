import requests
import time



def get_location(address, city=None, api_key=None, retry_times=3, delay=3):
    url = "https://restapi.amap.com/v3/geocode/geo"
    params = {
        'key': api_key,
        'address': address,
        'city':city
    }
    for attempt in range(retry_times):
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # 检查请求是否成功
            result = response.json()
            if result.get('status') == '1' and int(result.get('count', 0)) > 0:
                location = result['geocodes'][0]['location'].split(',')
                return {
                    "longitude": float(location[0]),
                    "latitude": float(location[1])
                }
            else:
                print(f"API返回非成功状态: {result.get('info')}")
                return {
                    "longitude": 0.1,
                    "latitude": 0.1
                }

        except requests.RequestException as e:
            print(f"请求出错 (尝试 {attempt + 1}/{retry_times}): {e}")
            if attempt < retry_times - 1:  # 不是最后一次尝试
                time.sleep(delay)  # 等待指定时间后重试
            else:
                print("达到最大重试次数，请求失败")
                return {
                    "longitude": 0.1,
                    "latitude": 0.1
                }
        except (KeyError, ValueError, IndexError) as e:
            print(f"解析响应出错: {e}")
            return {
                "longitude": 0.1,
                "latitude": 0.1
            }




def get_address(longitude, latitude, api_key=None, retry_times=3, delay=3):
    url = "https://restapi.amap.com/v3/geocode/regeo"
    params = {
        'key': api_key,
        'location': f"{longitude},{latitude}",
        'extensions': 'all'
    }
    for attempt in range(retry_times):
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # 检查请求是否成功
            result = response.json()

            if result.get('status') == '1' and result.get('regeocode'):
                regeocode = result['regeocode']
                address_component = regeocode.get('addressComponent', {})
                # 提取关键地址信息
                return {
                    "formatted_address": regeocode.get('formatted_address', ''),  # 完整地址
                    "province": address_component.get('province', ''),  # 省份
                    "city": address_component.get('city', ''),  # 城市
                    "district": address_component.get('district', ''),  # 区/县
                    "township": address_component.get('township', ''),  # 乡镇
                    "street": address_component.get('streetNumber', {}).get('street', ''),  # 街道
                    "number": address_component.get('streetNumber', {}).get('number', '')  # 门牌号
                }
            else:
                print(f"逆地理编码失败: {result.get('info')}")
                return None

        except requests.RequestException as e:
            print(f"请求出错 (尝试 {attempt + 1}/{retry_times}): {e}")
            if attempt < retry_times - 1:
                time.sleep(delay)
            else:
                print("达到最大重试次数，请求失败")
                return None
        except (KeyError, ValueError) as e:
            print(f"解析响应出错: {e}")
            return None




























if __name__ == "__main__":
    # 请替换为你的高德API密钥
    API_KEY = "f9d1fcc233de234630dd5f5b3e251d67"
    # location = get_location('武汉大学',city='武汉',api_key= "f9d1fcc233de234630dd5f5b3e251d67")
    location = get_address(114.287754,30.592186, api_key="f9d1fcc233de234630dd5f5b3e251d67")

    print(location)
