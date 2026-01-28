from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator, field_serializer
from typing import Literal


class Client(BaseModel):
    # 設定模型配置：允許使用 alias 或 field name 作為輸入
    model_config = ConfigDict(populate_by_name=True)

    # 定義類別參數
    name: str = Field(..., min_length=1, max_length=15,
                      alias="名稱", description="姓名或暱稱")
    gender: Literal["男", "女"] = Field(..., alias="性別", description="生理性別")
    age: Literal["18-30歲", "31-40歲", "41-50歲", "51-60歲",
                 "61-70歲"] = Field(..., alias="年紀", description="諮詢對象的年紀區間")
    area: Literal["北部（北北基桃竹）", "中部（苗中彰雲投）", "南部（嘉南高屏）", "東部（宜花東）", "離島"] = Field(
        ..., alias="地區", description="諮詢對象所在地區")
    location: str = Field(..., min_length=3, max_length=10,
                          alias="地點", description="更細部的地點，可以自行填入")
    mode: Literal["線上諮詢", "實體面談", "線上及實體皆可",
                  "其他"] = Field(..., alias="可接受諮詢方式", description="諮詢對象希望諮詢的方式")
    member: str = Field(..., min_length=2, max_length=15,
                        alias="所屬學員", description="是哪一位學員的朋友")

    @field_validator('member', 'location', mode='before')
    @classmethod
    def allow_int_as_str(cls, v):
        if isinstance(v, (int, float)):
            return str(int(v)) if isinstance(v, int) or v.is_integer() else str(v)
        return v
    status: Literal["待預約",
                    "已預約", "已取消"] = Field(..., alias="預約狀態", description="諮詢對象目前是否已被預約")
    remark: str = Field(default="", max_length=30,
                        alias="備註", description="其他補充說明")
    update_time: datetime = Field(
        default_factory=datetime.now, alias="更新時間", description="資料最後更新的時間")

    @field_validator('update_time', mode='before')
    @classmethod
    def parse_update_time(cls, v):
        """將字串格式的時間轉換為 datetime 物件"""
        if isinstance(v, str):
            if not v or v.strip() == "":
                return datetime.now()
            try:
                return datetime.strptime(v, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                # 嘗試其他可能的格式
                try:
                    return datetime.strptime(v, "%Y/%m/%d %H:%M:%S")
                except ValueError:
                    return datetime.now()
        return v

    @field_serializer('update_time')
    def serialize_update_time(self, dt):
        """序列化時間欄位，確保輸出為字串格式"""
        # 如果已經是字串，直接返回
        if isinstance(dt, str):
            return dt
        # 如果是 datetime 物件，轉換為字串
        if isinstance(dt, datetime):
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        # 其他情況返回當前時間
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def touch(self):
        """手動觸發時間更新"""
        self.update_time = datetime.now()
