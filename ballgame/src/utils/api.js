// 统一处理与后端的信息

//引入axios
import axios from 'axios'
// 引入ui组件Message，是一个弹窗
import { Message } from 'element-ui';
//引入登录路由配置
import router from '../router'


//响应拦截器
axios.interceptors.response.use(success=>{
    //成功调到后端接口
    //后端会传三个信息，响应码，响应信息，data（数据）
    if(success.status && success.status == 200){
      //错误情况
      if(success.data.code==500||success.data.code==401||success.data.code==403){
        //判断三个响应码（实际有很多，假设其他情况都是正常）
        Message.error({message:success.data.message});
        //正确情况
        if(success.data.message){
          //如果后端反馈信息了,那我们就显示这个信息提示用户
          Message.success({message:success.data.message});
        }
        return success.data;
      }
    }

  },
  //后端接口掉入失败
  error=> {
    //同理只列举几种情况,504表示服务器有问题，404表示页面找不到
    if (error.response.code == 504) {
      Message.error({message:'服务器走丢了，大概率是没钱了o(╯□╰)o'});
    }
    else if(error.response.code == 403){
      Message.error({message:'小伙子，你的权限不够，请联系管理员！'});
    }
    else if(error.response.code==401){
      Message.error({message:'没有登录哦！'});
      //帮用户去到登录页面
      router.replace('/');
    }
    else{
      if(error.response.message){
        //如果后端返回了信息,就把信息显示给用户
        Message.error({message:error.response.data.message});
      }
      else{
        Message.error({message:'未知错误'});
      }
    }
    return;
  }
);

//传送json的post请求
export const postRequest=(url,params)=>{
  return axios({
      method:'post',
      url:'${url}',
      data:params
    }
  )
}

