
Max = [[7,5,3],
       [3,2,2],
       [9,0,2],
       [2,2,2],
       [4,3,3]]

Allocation = [[0,1,1],
              [2,0,0],
              [3,0,2],
              [2,1,1],
              [0,0,2]]

Need = [[7,4,3],
        [1,2,2],
        [6,0,0],
        [0,1,1],
        [4,3,1]]

Available = [3,3,2]


def re2nd(re:list,i:int,nd:list):
    ND = nd[i]
    for j in range(len(re)):
        if re[j] <= ND[j]:
            continue
        else:
            print('请求失败，所需资源超过所宣布最大值')
            return False
    return True

def re2av(re:list,av:list):
    for j in range(len(re)):
        if re[j] <= av[j]:
            continue
        else:
            print('请求失败，当前可用资源不足，请等待')
            return False
    return True



def PreAllocate(nd:list, av:list, al:list, re:list):
    nd_p = nd
    av_p = av
    al_p = al
    re_p = re
    for i in range(len(al_p)):
        for j in range(len(re_p)):
            al_p[i][j] += re_p[j]
            nd_p[i][j] -= re_p[j]
            av_p[j] -= re_p[j]
    if SafetyDetect(nd_p,av_p,al_p):
        nd = nd_p
        av = av_p
        al = al_p
        print('请求成功，已分配')
        return True
    else:
        print('预分配失败，不安全状态')
        return False




def SafetyDetect(nd:list,av:list,al:list):
    # step 1
    work = av
    finish = [False]*len(nd)
    all_true_flag = False

    # step 2
    while(not all_true_flag):
        for i in range(len(nd)):
            if finish[i]==False:
                miniflag = 0
                for j in range(len(work)):
                    if nd[i][j] <= work[j]:
                        miniflag+=1
                    else:
                        break
                if miniflag == len(work):
                    # step 3
                    for j in range(len(work)):
                        work[j] += al[i][j]
                        finish[i] = True
        for f in finish:
            if f == False:
                return False
            else:
                all_true_flag=True
                continue
    return True





if __name__ =='__main__':

    Request = [1, 0, 2]

    re2nd(Request,1,Need)
    re2av(Request,Available)
    PreAllocate(Need,Available,Allocation,Request)
