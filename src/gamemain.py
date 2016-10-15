
import unit
#from unit import UnitObject
MAX_ROUND=1000
class GameMain:
    units = {}  # 单位dict key:unit_id value:unitobject
    hqs = []  # 主基地
    buildings = []  # 中立建筑
    #turn_flag = 0  # 谁的回合
    turn_num = 0  # 回合数
    phase_num = 0  # 回合阶段指示
    skill_instr_0=[]#ai0的当前回合指令
    skill_instr_1=[]#ai1的当前回合制令
    produce_instr_0=[]
    produce_instr_1=[]
    move_instr_0=[]#指令格式[[unit_id,position_x,position_y],[unit_id,position_x,position_y]]
    move_instr_1=[]
    capture_instr_0=[]#指令格式[[unit_id,building_id][unit_id,building_id][]]
    capture_instr_1=[]
    buff = {
        unit.FLAG_0: {
            unit.INFANTRY: {'health_buff': 0.0, 'attack_buff': 0.0, 'speed_buff': 0.0, 'defense_buff': 0.0,
                       'shot_range_buff': 0.0,'produce_buff':0.0},
            unit.VEHICLE: {'health_buff': 0.0, 'attack_buff': 0.0, 'speed_buff': 0.0, 'defense_buff': 0.0,
                      'shot_range_buff': 0.0,'produce_buff':0.0},
            unit.AIRCRAFT: {'health_buff': 0.0, 'attack_buff': 0.0, 'speed_buff': 0.0, 'defense_buff': 0.0,
                       'shot_range_buff': 0.0,'produce_buff':0.0}
        },
        unit.FLAG_1: {
            unit.INFANTRY: {'health_buff': 0.0, 'attack_buff': 0.0, 'speed_buff': 0.0, 'defense_buff': 0.0,
                       'shot_range_buff': 0.0,'produce_buff':0.0},
            unit.VEHICLE: {'health_buff': 0.0, 'attack_buff': 0.0, 'speed_buff': 0.0, 'defense_buff': 0.0,
                      'shot_range_buff': 0.0,'produce_buff':0.0},
            unit.AIRCRAFT: {'health_buff': 0.0, 'attack_buff': 0.0, 'speed_buff': 0.0, 'defense_buff': 0.0,
                       'shot_range_buff': 0.0,'produce_buff':0.0}
        }
    }

    def __init__(self):
        pass

    def win_determine(self):
        # 胜利判定:0 ai_id0 wins; 1 ai_id1 wins; 2 tie; 3 game goes on
        unit_obj = list(self.units.values())#所有的单位
        flag_0=self.hqs[0].flag
        flag_1=self.hqs[1].flag
        counter_01=0 # 0方的兵力
        counter_11=0 # 1方的兵力
        counter_02=0 # 0方的建筑数
        counter_12=0 # 1方的建筑数
        if self.hqs[0].health_now*self.hqs[1].health_now>0 and self.hqs[0].health_now+self.hqs[1].health_now>0:#如果双方主基地都正Hp
            return 3
        else:
            if self.hqs[0].health_now<self.hqs[1].health_now:
                return 1
            if self.hqs[0].health_now > self.hqs[1].health_now:
                return 0
            if self.hqs[0].health_now == self.hqs[1].health_now:
                for things in unit_obj:
                    if things.__unit_type==1 or things.__unit_type==2 or things.__unit_type==3:
                        if things.flag==flag_0:
                            counter_01+=1
                        if things.flag==flag_1:
                            counter_11+=1
                    else:
                        if things.flag==flag_0:
                            counter_02 += 1
                        if things.flag == flag_1:
                            counter_12 +=1
                    if counter_01>counter_11:
                        return 0
                    if counter_01<counter_11:
                        return 1
                    if counter_01==counter_11:
                        if counter_02>counter_12:
                            return 0
                        if counter_02<counter_12:
                            return 1
                        if counter_02==counter_12:
                            return 2

    def timeup_determine(self):
        #超时胜利判定
        if self.turn_num>MAX_ROUND:#如果超过了最大回合数
            unit_obj = list(self.units.values())
            flag_0 = self.hqs[0].flag
            flag_1 = self.hqs[1].flag
            counter_01 = 0  # 0方的兵力
            counter_11 = 0  # 1方的兵力
            counter_02 = 0  # 0方的建筑数
            counter_12 = 0  # 1方的建筑数
            if self.hqs[0].health_now < self.hqs[1].health_now:
                return 1
            if self.hqs[0].health_now > self.hqs[1].health_now:
                return 0
            if self.hqs[0].health_now == self.hqs[1].health_now:
                for things in unit_obj:
                    if things.__unit_type == 1 or things.__unit_type == 2 or things.__unit_type == 3:
                        if things.flag == flag_0:
                            counter_01 += 1
                        if things.flag == flag_1:
                            counter_11 += 1
                    else:
                        if things.flag == flag_0:
                            counter_02 += 1
                        if things.flag == flag_1:
                            counter_12 += 1
                    if counter_01 > counter_11:
                        return 0
                    if counter_01 < counter_11:
                        return 1
                    if counter_01 == counter_11:
                        if counter_02 > counter_12:
                            return 0
                        if counter_02 < counter_12:
                            return 1
                        if counter_02 == counter_12:
                            return 2

    def cleanup_phase(self):
        # 单位死亡判定

        pass

    def skill_phase(selfself):
        # 技能结算

        pass

    def move_phase(self):
        # 移动指令结算
        id_collection = list(self.units.values())  # 寻找传入ai_id对应的value(unitobject)
        for things in self.move_instr_0:
            for obj in id_collection:
                if obj.unit_id == things[0]:  # 如果unit_id 相符
                    if obj.__unit_type == 0 or obj.__unit_type == 4 or obj.flag!=0:
                        pass
                    else:
                        x = things[1]
                        y = things[2]
                        x1 = obj.position_x
                        y1 = obj.position_y
                        if x > 100 or y > 100 or x < 0 or y < 0:
                            return
                        elif abs(x1 - x) + abs(y1 - y) <= obj.max_speed_now:
                            for obj_1 in id_collection:
                                if obj_1.position_x==x and obj_1.position_y==y:
                                    pass
                                else :
                                    obj.position_x = x
                                    obj.position_y = y
                        else:
                            pass
        for things in self.move_instr_1:
            for obj in id_collection:
                if obj.unit_id == things[0]:  # 如果unit_id 相符
                    if obj.__unit_type == 0 or obj.__unit_type == 4 or obj.flag==0:
                        pass
                    else:
                        x = things[1]
                        y = things[2]
                        x1 = obj.position_x
                        y1 = obj.position_y
                        if x > 100 or y > 100 or x < 0 or y < 0:
                            return
                        elif abs(x1 - x) + abs(y1 - y) <= obj.max_speed_now:
                            for obj_1 in id_collection:
                                if obj_1.position_x==x and obj_1.position_y==y:
                                    pass
                                else :
                                    obj.position_x = x
                                    obj.position_y = y
                        else:
                            pass

    def produce_phase(self):
        # 兵种获取指令结算

        pass

    def capture_phase(self):
        # 占领建筑阶段
        unit_obj = list(self.units.values())
        for orders in self.capture_instr_0:
            for things in unit_obj:
                if orders[0]==things.unit_id and things.__type_name=="meat" and things.flag==0:
                    for k in unit_obj:
                        if k.unit_id==orders[1] and k.__unit_type==4 and abs(things.position_x-k.position_x)+abs(things.position_y-k.position_y)==1:
                            things.current_pointer+=1
        for orders in self.capture_instr_1:
            for things in unit_obj:
                if orders[0]==things.unit_id and things.__type_name=="meat" and things.flag==1:
                    for k in unit_obj:
                        if k.unit_id==orders[1] and k.__unit_type==4 and abs(things.position_x-k.position_x)+abs(things.position_y-k.position_y)==1:
                            things.current_pointer-=1
        for obj in unit_obj:#结算建筑都是哪一方的
            if obj.current_pointer>0:
                obj.flag=0
            if obj.current_pointer<0:
                obj.flag=1
            if obj.current_pointer==0 and obj.__type_name==4:
                obj.flag=2
            for unit in unit_obj:
                if unit.__type_name=='hack_lab':
                    for things in unit_obj:
                        if things.flag==unit.flag:
                            things.hacked_point*=1.5
                if unit.__type_name=='bid_lab':
                    if unit.flag==0:
                        self.buff[unit.FLAG_0[unit.INFANTRY['health_buff']]]=0.5
                    if unit.flag==1:
                        self.buff[unit.FLAG_1[unit.INFANTRY['health_buff']]] = 0.5
                if unit.__type_name=='car_lab':
                    if unit.flag==0:
                        self.buff[unit.FLAG_0[unit.VEHICLE['attack_buff']]]=0.05
                        self.buff[unit.FLAG_0[unit.VEHICLE['defence_buff']]] = 0.05
                    if unit.flag==1:
                        self.buff[unit.FLAG_1[unit.VEHICLE['attack_buff']]] = 0.05
                        self.buff[unit.FLAG_1[unit.VEHICLE['defence_buff']]] = 0.05
                if unit.__type_name == 'elec_lab':
                    if unit.flag==0:
                        self.buff[unit.FLAG_0[unit.VEHICLE['attack_buff']]]=0.1
                        self.buff[unit.FLAG_0[unit.AIRCRAFT['attack_buff']]]=0.1
                    if unit.flag==1:
                        self.buff[unit.FLAG_1[unit.VEHICLE['attack_buff']]]=0.1
                        self.buff[unit.FLAG_1[unit.AIRCRAFT['attack_buff']]]=0.1
                if unit.__type_name == 'radiation_lab':
                    if unit.flag==0:
                        self.buff[unit.FLAG_0[unit.VEHICLE['attack_buff']]]=0.2


                    if unit.flag==1:
                        self.buff[unit.FLAG_1[unit.VEHICLE['attack_buff']]]=0.2

                if unit.__type_name == 'uav_lab':
                    if unit.flag == 0:
                        self.buff[unit.FLAG_0[unit.VEHICLE['produce_buff']]] = 0.15
                        self.buff[unit.FLAG_0[unit.INFANTRY['produce_buff']]] = 0.15
                        self.buff[unit.FLAG_0[unit.AIRCRAFT['produce_buff']]] = 0.15

                    if unit.flag == 1:
                        self.buff[unit.FLAG_1[unit.VEHICLE['produce_buff']]] = 0.15
                        self.buff[unit.FLAG_1[unit.INFANTRY['produce_buff']]] = 0.15
                        self.buff[unit.FLAG_1[unit.AIRCRAFT['produce_buff']]] = 0.15
                if unit.__type_name == 'aircraft_lab':
                    if unit.flag == 0:
                        self.buff[unit.FLAG_0[unit.AIRCRAFT['produce_buff']]] = 0.1
                        self.buff[unit.FLAG_0[unit.AIRCRAFT['speed_buff']]] = 3
                        self.buff[unit.FLAG_0[unit.AIRCRAFT['attack_buff']]] = 0.1
                    if unit.flag == 1:
                        self.buff[unit.FLAG_1[unit.VEHICLE['produce_buff']]] = 0.1
                        self.buff[unit.FLAG_1[unit.VEHICLE['speed_buff']]] = 3
                        self.buff[unit.FLAG_1[unit.VEHICLE['attack_buff']]] = 0.1
















      #  'hack_lab':9, 'bid_lab':10, 'car_lab':11, 'elec_lab':12, 'radiation_lab':13, 'uav_lab':14, 'aircraft_lab':15,
        #           'build_lab':16,'finance_lab':17,'material_lab':18,'nano_lab':19}










        pass

    def fetch_instruction(self):
        #获取指令存入两个指令list
        pass

    def check_legal(self):
        #检查双方指令是否合法，去重
        #将指令list反向
        self.move_instr_0.reverse()
        self.move_instr_1.reverse()
        self.capture_instr_0.reverse()
        self.capture_instr_1.reverse()
        self.skill_instr_0.reverse()
        self.skill_instr_1.reverse()
        self.produce_instr_0.reverse()
        self.produce_instr_1.reverse()
        for i in range(len(self.move_instr_0)):
            for things in self.units.values():
                if things.unit_id==self.move_instr_0[i][0] and things.flag==0:#如果移动的是自己的单位
                    for j in range[i:len(self.move_instr_0):1]:
                        if self.move_instr_0[i][0]==self.move_instr_0[j][0]:#如果unit_id相同
                            del self.move_instr_0[j]#删除较靠前的项
                if things.unit_id==self.move_instr_0[i][0] and things.flag==1:#如果移动的不是自己的单位
                    del self.move_instr_0[i]
        for i in range(len(self.move_instr_1)):
            for things in self.units.values():
                if things.unit_id==self.move_instr_1[i][0] and things.flag==1:#如果移动的是自己的单位
                    for j in range[i:len(self.move_instr_1):1]:
                        if self.move_instr_1[i][0]==self.move_instr_1[j][0]:#如果unit_id相同
                            del self.move_instr_1[j]#删除较靠前的项
                if things.unit_id==self.move_instr_1[i][0] and things.flag==0:#如果移动的不是自己的单位
                    del self.move_instr_1[i]
        self.move_instr_0.reverse()
        self.move_instr_1.reverse()
        for i in range(len(self.capture_instr_0)):
            for things in self.units.values():
                if things.unit_id==self.capture_instr_0[i][0] and things.flag==0:#如果移动的是自己的单位
                    for j in range[i:len(self.capture_instr_0):1]:
                        if self.capture_instr_0[i][0]==self.capture_instr_0[j][0]:#如果unit_id相同
                            del self.capture_instr_0[j]#删除较靠前的项
                if things.unit_id==self.capture_instr_0[i][0] and things.flag==1:#如果移动的不是自己的单位
                    del self.capture_instr_0[i]#删除该指令
        for i in range(len(self.capture_instr_1)):
            for things in self.units.values():
                if things.unit_id==self.capture_instr_1[i][0] and things.flag==1:#如果移动的是自己的单位
                    for j in range[i:len(self.capture_instr_1):1]:
                        if self.capture_instr_1[i][0]==self.capture_instr_1[j][0]:#如果unit_id相同
                            del self.capture_instr_1[j]#删除较靠前的项
                if things.unit_id==self.capture_instr_1[i][0] and things.flag==0:#如果移动的不是自己的单位
                    del self.capture_instr_1[i]#删除该指令
        self.capture_instr_0.reverse()
        self.capture_instr_1.reverse()
        for i in range(len(self.produce_instr_0)):
            for things in self.units.values():
                if things.unit_id==self.produce_instr_0[i][0] and things.flag==0:#如果移动的是自己的单位
                    for j in range[i:len(self.produce_instr_0):1]:
                        if self.produce_instr_0[i][0]==self.produce_instr_0[j][0]:#如果unit_id相同
                            del self.capture_instr_0[j]#删除较靠前的项
                if things.unit_id==self.produce_instr_0[i][0] and things.flag==1:#如果移动的不是自己的单位
                    del self.produce_instr_0[i]#删除该指令
        for i in range(len(self.produce_instr_1)):
            for things in self.units.values():
                if things.unit_id==self.produce_instr_1[i][0] and things.flag==1:#如果移动的是自己的单位
                    for j in range[i:len(self.produce_instr_1):1]:
                        if self.produce_instr_1[i][0]==self.produce_instr_1[j][0]:#如果unit_id相同
                            del self.produce_instr_1[j]#删除较靠前的项
                if things.unit_id==self.produce_instr_1[i][0] and things.flag==0:#如果移动的不是自己的单位
                    del self.produce_instr_1[i]#删除该指令
        self.produce_instr_0.reverse()
        self.produce_instr_1.reverse()
        for i in range(len(self.skill_instr_0)):
            for things in self.units.values():
                if things.unit_id==self.skill_instr_0[i][0] and things.flag==0:#如果移动的是自己的单位
                    for j in range[i:len(self.skill_instr_0):1]:
                        if self.skill_instr_0[i][0]==self.skill_instr_0[j][0]:#如果unit_id相同
                            del self.capture_instr_0[j]#删除较靠前的项
                if things.unit_id==self.skill_instr_0[i][0] and things.flag==1:#如果移动的不是自己的单位
                    del self.skill_instr_0[i]#删除该指令
        for i in range(len(self.skill_instr_1)):
            for things in self.units.values():
                if things.unit_id==self.skill_instr_1[i][0] and things.flag==1:#如果移动的是自己的单位
                    for j in range[i:len(self.skill_instr_1):1]:
                        if self.skill_instr_1[i][0]==self.skill_instr_1[j][0]:#如果unit_id相同
                            del self.skill_instr_1[j]#删除较靠前的项
                if things.unit_id==self.skill_instr_1[i][0] and things.flag==0:#如果移动的不是自己的单位
                    del self.skill_instr_1[i]#删除该指令
        self.skill_instr_0.reverse()
        self.skill_instr_1.reverse()

        pass


    def next_tick(self):
        # 获取指令，指令检测合法与去重，回合演算
        self.check_legal()
        self.skill_phase()
        self.cleanup_phase()
        self.win_determine()
        self.move_phase()
        self.produce_phase()
        self.capture_phase()
        self.timeup_determine()
        pass

    def to_string(self):
        # 将当前状态信息返回，用String,Json什么都行，你们自己起名字吧
        pass


