from datetime import datetime
from pydantic import BaseModel, Field, field_validator, field_serializer
from typing import Literal


class Client(BaseModel):
    # 定義類別參數
    name: str = Field(..., min_length=1, max_length=15,
                      alias="名稱", description="姓名或暱稱")
    gender: Literal["男", "女"] = Field(..., alias="性別", description="生理性別")
    age: int = Field(..., gt=0, lt=100, alias="年紀", description="年紀")
    area: Literal["北部", "中部", "南部", "東部", "離島"] = Field(
        ..., alias="地區", description="諮詢對象所在地區")
    location: str = Field(..., min_length=3, max_length=10,
                          alias="地點", description="更細部的地點，可以自行填入")
    mode: Literal["線上諮詢", "實體面談", "線上及實體皆可",
                  "其他"] = Field(..., alias="可接受諮詢方式", description="諮詢對象希望諮詢的方式")
    member: str = Field(..., min_length=2, max_length=15,
                        alias="所屬學員", description="是哪一位學員的朋友")
    status: Literal["待預約",
                    "已預約"] = Field(..., alias="預約狀態", description="諮詢對象目前是否已被預約")
    remark: str = Field(max_length=30, alias="備註", description="其他補充說明")
    update_time: datetime = Field(
        default_factory=datetime.now, alias="更新時間", description="資料最後更新的時間")

    @field_serializer('update_time')
    def serialize_update_time(self, dt: datetime):
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    def touch(self):
        """手動觸發時間更新"""
        self.update_time = datetime.now()
