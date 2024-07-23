<template>
    <body class="bg-1">
 

        <!-- Wrap all page content here -->
        <div id="wrap">
          <!-- Make page fluid -->
          <div class="row">
            <!-- Page content -->
            <div id="content" class="col-md-12 full-page login">
    
    
              <div class="inside-block">
                <img src="../../static/images/logo-big.png" alt class="logo">
                <h1>欢迎&nbsp;&nbsp;登录</h1>
                <h4>合作网络分析系统</h4>
    
                <el-form ref="loginFormRef" :model="loginForm" label-width="0px" class="login_form" :rules="loginFormRules">
                    <!-- 用户名 -->
                   
                    <el-form-item prop="username">
                        <div class="input-group">
                        <div class="input-group-addon"><i class="el-icon-user"></i></div>
                        <el-input   v-model="loginForm.username" ></el-input>
                        </div>
                    </el-form-item>
                    
                    <!-- 密码 -->
                    <el-form-item prop="password">
                        <div class="input-group">
                        <div class="input-group-addon"><i class="el-icon-lock"></i></div>
                        <el-input v-model="loginForm.password" type="password"></el-input>
                        </div>
                       
                    </el-form-item>

                    
                    
                    <!-- 登录和重置 -->
                    <el-form-item class="btns">
                        <el-button type="primary" @click="validForm">登录</el-button>
                       
                        <el-button type="info" @click="resetLoginFrom" style="margin-left: 135px;">重置</el-button>
                    </el-form-item>
                </el-form>
              </div>
    
    
            </div>
            <!-- /Page content -->  
          </div>
        </div>
        <!-- Wrap all page content end -->
      </body>
</template>

<script>
    export default {
        name: 'Login',
        data(){
            return {
            loginForm:{
                username:'neo4j',
                password:'58094894'

                },
            loginFormRules:{
                username:[
                { required: true, message: '请输入登录名称', trigger: 'blur' },
                {min:2 ,message:"长度在2个字符以上"}
                 
                ],
                password:[
                { required: true, message: '请输入密码', trigger: 'blur' },
                {min:2 ,message:"长度在2个字符以上"}
                ]
            }
            };
        },
        methods:{
            // 重置表单
            resetLoginFrom(){
                this.$refs.loginFormRef.resetFields();

            },
            validForm(){
                this.$refs.loginFormRef.validate(async valid=>{
                    if(!valid)
                        return ;
                    
                    const {data:res}=await this.$axios.post('login/',this.loginForm,{dataType:'json'});
                    if(res.status!==200)
                        this.$message.error(res.data);
                    else{
                    console.log(res)
                    this.$message.success(res.data);
                    window.sessionStorage.setItem('token',res.token);
                    this.$router.push('/home');
                    }
                    


                    
                });

            }
        }
    };
</script>

<style lang="less" scoped>
   
 
    .btns{
        display: flex;
        justify-content: flex-end;
       

    }
    .login_form{
        
        position: relative;
        bottom: 0;
        
        width: 100%;
        padding: 0 40px ;
        box-sizing: border-box;


    }

</style>