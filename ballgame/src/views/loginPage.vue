<template>
  <!--放背景图-->
  <div class="background">
    <!--tab切换页面-->
    <el-tabs type="border-card" class="loginContainer">

      <!--登录页面-->
      <el-tab-pane label="登录" >
        <h1 class="Title" >E知论文管理系统</h1>
        <div>
          <div>
            <el-form
                :model="loginFormData"
                :rules="loginRules"
                label-width="200px"
                label-position="top"
                ref="form1"
            >
              <el-form-item prop="account" label="邮箱">
                <el-input placeholder="邮箱"
                          v-model="loginFormData.account"
                >
                </el-input>
              </el-form-item>

              <el-form-item prop="password" label="密码">
                <!--监听回车事件-->
                <el-input
                    @keyup.enter.native="submitLogin()"
                    placeholder="密码"
                    type="password"
                    v-model="loginFormData.password"
                >
                </el-input>
              </el-form-item>

              <div class="btn">
                <el-button @click="submitLogin()" type="primary" class="loginbtn">登录</el-button>
              </div>
            </el-form>
          </div>
        </div>
      </el-tab-pane>

      <!--注册页面-->
      <el-tab-pane label="注册">
        <h1 class="Title">论文管理系统</h1>
        <div>
          <div>
            <el-form
                :model="registerFormData"
                :rules="registerRules"
                label-width="100px"
                label-position="left"
                ref="form2"
            >
              <el-form-item prop="userName" label="用户名">
                <el-input placeholder="用户名" v-model="registerFormData.userName">
                </el-input>
              </el-form-item>

              <el-form-item prop="userAccount" label="邮箱">
                <el-input placeholder="邮箱" v-model="registerFormData.userAccount">
                </el-input>
              </el-form-item>

              <el-form-item prop="userPassword" label="密码">
                <el-input
                    @keyup.enter.native="submitRegister()"
                    placeholder="密码"
                    type="password"
                    v-model="registerFormData.userPassword"
                >
                </el-input>
              </el-form-item>

              <el-form-item prop="checkuserPassword" label="确认密码">
                <el-input type="password"
                          v-model="registerFormData.checkuserPassword"
                          @keyup.enter.native="submitRegister()"
                          placeholder="再次输入密码"
                >
                </el-input>
              </el-form-item>

              <el-form-item label="验证码">
                <el-input placeholder="验证码"
                          v-model="registerFormData.code"
                          @keyup.enter.native="submitLogin()"
                          style="width:130px;margin-right: 10px"
                          prop="code"
                >
                </el-input>
                <el-button type="success" round
                           @click="sendCode"
                           style="margin-left:5px"
                >
                  发送验证码
                </el-button>
              </el-form-item>

              <div class="btn">
                <el-button @click="submitRegister()"
                           type="primary">
                  注册
                </el-button>
              </div>
            </el-form>
          </div>
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import {isEmail} from "../utils/validate"
export default {
  name: "loginPage",
  data: function() {

    //检验两次输入的密码是否一致
    var validateCheckuserPassword = (rule, value, callback) => {
      if (value !== this.registerFormData.userPassword) {
        callback(new Error('两次输入密码不一致!'));
      } else {
        callback();
      }
    };

    //检验邮箱格式
    let validateEmail = (rule, value, callback) => {
      if (!isEmail(value)) {
        callback(new Error('邮箱格式错误'))
      } else {
        callback()
      }
    }

    return {
      //背景图
      imgSrc:require('../assets/img/star.png'),

      loginFormData: {
        account: "2540590989@qq.com",
        password: "123",
        userType:"1"
      },

      registerFormData:{
        userName:"yxw",
        userAccount:"2540590989@qq.com",
        userPassword:"123",
        checkuserPassword:"123",
        code:""
      },

      loginRules: {
        account: [
          {required: true, message: '邮箱不能为空', trigger: 'blur'},
          {validator: validateEmail, trigger: 'blur'}
        ],
        password: [{ required: true, message: "请输入密码", trigger: "blur" }],
        userType: [
          { required: true, message: "请选择用户类型", trigger: "blur" }
        ]
      },

      registerRules: {
        userAccount: [
          {required: true, message: '邮箱不能为空', trigger: 'blur'},
          {validator: validateEmail, trigger: 'blur'}
        ],
        userPassword: [{ required: true, message: "密码不能为空", trigger: "blur" }],
        checkuserPassword:
            [
              { required: true, message: "请再次输入密码", trigger: "blur" },
              { validator: validateCheckuserPassword, trigger: 'blur' }
            ],
        userName: [
          { required: true, message: "请输入用户名", trigger: "blur" }
        ],
      }
    };
  },
  methods: {
    submitLogin() {
      this.$refs.form1.validate(valid => {
        if (valid) {
          //向后端发出请求
          this.$axios.post("http://127.0.0.1:8000/api/login/",
              {
                "userName": this.registerFormData.userName,
                "password": this.registerFormData.userPassword
              }).then((response) => {
            if (response.data.status == 200) {
              this.$message.success("成功登录!");
            } else {
              this.$message.error("密码或账号错误")
            }
          })
        } else {
          this.$message.error("请完整输入所有信息！");
          return false;
        }
      })
    },

    sendCode() {
      this.$refs.form2.validate(valid => {
        if (valid) {
          //向后端发出请求
          this.$axios.post("/api/user/register",
              {"userName":this.registerFormData.userName,"userAccount":this.registerFormData.userAccount,"userPassword":this.registerFormData.userPassword}).then((response) => {
            if(response.data.status==100) {
              this.$message.success("验证码已发送!");
            }
            else if(response.data.status==1006){
              this.$message.error("邮箱已被注册！")
            }
            else{
              this.$message.error("系统错误，检查一下redis是否已经在运行")
            }
          })
        }
        else{
          this.$message.error("请完整输入所有信息！");
          return false;
        }
      });
    },

    submitRegister(){
      this.$axios.put("/api/user/verify/"+this.registerFormData.code
      ).then((response) => {
        if(response.data.status==100){
          this.$message.success("注册成功，现在去登录吧！");
        }
        else{
          this.$message.error("注册失败，请联系管理员！");
        }
      })
    }

  }
}
</script>

<style scoped>
.background{
  width: 100%;height: 100%;
  background-image: url("../assets/img/loginBackground.png");
  background-size: cover; /* 使图片平铺满整个浏览器（从宽和高的最大需求方面来满足，会使某些部分无法显示在区域中） */
  position: absolute; /* 不可缺少 */
  /* overflow: hidden; */
  /* overflow: auto; */
  z-index: -1;
  background-repeat: no-repeat;
}
.loginContainer{
  border-radius: 30px;
  background-clip:padding-box;
  margin:180px auto;
  width:400px;
  height:500px;
  padding :15px 35px 15px 35px;
  background: rgba(255, 255, 255, 0.49);
  border:1px solid #eaeaea;
  box-shadow: 0 0 25px #cac6c6
}

.Title{
  margin: 0px auto 40px auto;
  text-align: center;
  font-family:华文楷体;
  fort-size:100px;
  color: rgba(0, 3, 7, 0.99);
}

.loginbtn{
  margin-top: 30px;
}
.btn button {
  width: 100%;
  height: 36px;
}
</style>