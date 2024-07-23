<template>
    
    <div id="content" class="col-md-12" style="margin-top: 30px; " >
        
        <el-row :gutter="20" style=" margin-right:250px">
            <el-col :span="6" :offset="6" >
               <!-- <el-input placeholder="请输入关键词" id="key" v-model="input">
                </el-input> -->
                <el-select v-model="input" filterable placeholder="选择关键词" @change="drawt()">
                    <el-option
                      v-for="item in option_key"
                      :key="item.value"
                      :value="item.value">
                    </el-option>
                </el-select>
             
            </el-col>
            <el-col :span="3">
                <el-dropdown>
                    <el-button  icon="el-icon-picture">
                       绘制<i class="el-icon-arrow-down el-icon--right"></i>
                    </el-button>
                    <el-dropdown-menu slot="dropdown" >
                      <el-dropdown-item  @click.native="choose('country')">国家</el-dropdown-item>
                      <el-dropdown-item  @click.native="choose('institution')">机构</el-dropdown-item>
                      <el-dropdown-item  @click.native="choose('author')">作者</el-dropdown-item>
                    </el-dropdown-menu>
                   
                </el-dropdown>
               
            </el-col>
            <el-col :span="2" >
                <el-button  >
                    节点颜色
                </el-button>
                
            </el-col>
            <el-col :span="1">
                <el-color-picker v-model="color1" size="big" @change="change(value)"></el-color-picker>
            </el-col>

           
            <el-col :span="2" >
                <el-button  >
                    &nbsp 边颜色&nbsp
                </el-button>
            </el-col>
            <el-col :span="1">
                <el-color-picker v-model="color2" size="big" @change="change(value)"></el-color-picker>
            </el-col>
           
         
            
        </el-row>
        
    <section  class="tile transparent" style=" margin-right:250px;margin-top: 30px;"  >
        <div class="tile-widget color transparent-black textured">
            <div class="table-responsive" align="center">
                <div id="chart_lz_region" style="width: 100%; height: 600px;">
                    <div ref="viz" id="viz" style="width:100%;height:100%">
                    </div>
                </div>
    </div>
    </div >
    </section >
    </div>

</template>

<script>
    // import NeoVis from 'neovis.js/dist/neovis.js'
    import { neourl } from '../setting.js'
    export default {
        name: 'display',
        data(){
            return {
                vis:{},
                choice:'',
                sentence:'',
                color1: '#409EFF',
                color2: '#409EFF',
                input:'',
                option_key:[]
            }
        },

        
        mounted() { 
            this.get_keyword()
        }, //渲染
        methods: {
            
            draw () {
                // config 配置项
                const loading = this.$loading({
                lock: true,
                text: 'Loading',
                spinner: 'el-icon-loading',
                background: 'rgba(0, 0, 0, 0.7)'
                });
                
                var config = {
                    container_id: 'viz', //dom元素id
                    // neo4j服务器地址，用户名 和 密码
                    server_url:  neourl, //连接的地址是端口号为7687的不是7474
                    server_user: 'neo4j',
                    server_password: '58094894',
                    // labels是节点样式的配置
                    // 没有在这个地方配置的节点将会是默认样式
                    
                    labels: {
                        author: {
                        
                            caption: 'name',  
                            size: 'number', 
                        
                        },
                        country: {
                        
                            caption: 'name',  
                            size: 'number', 

                        },
                        institution: {
                        
                            caption: 'name',  
                            size: 'number',   
                        
                        },
                    
                    },
                   
                    relationships: {
                        cooperate:{
                            thickness: 'number',  //String：线段粗细，用作边缘厚度的属性名。默认为1。
                            caption: true,  //Boolean：如果设置为true，则关系类型将显示为边缘标题。或String：用作边缘标题的属性名。
                            font: { size: 12, color: '#606266' }  // 关系节点文字大小颜色
   
                            
                        },
                    

                    },
                   
                    // 关系线段是否显示箭头
                    arrows: false,
            
                    hierarchical: false, // 节点显示方式 是否启用分层布局后
                    // 分层结构或者默认 "hubsize"（默认）和"directed".
                    hierarchical_sort_method: 'directed',
                    encrypted: 'ENCRYPTION_OFF', // "ENCRYPTION_OFF" (default) or "ENCRYPTION_ON"
                    trust: 'TRUST_ALL_CERTIFICATES', // "TRUST_ALL_CERTIFICATES" (default) or "TRUST_SYSTEM_CA_SIGNED_CERTIFICATES"
                    // 配置数据库查询语句, 替换成自己的查询语句才可以显示
                    initial_cypher: this.sentence
                }
                const newConfig = new NeoVis.migrateFromOldConfig(config);
                // console.log(newConfig)
                newConfig.visConfig =  {
                    edges: {
                        arrows: {
                            to: {enabled: false}
                        },
                        color:this.color2
                    },
                    nodes: {
                        shape: 'dot',
                        color:this.color1,
                        scaling:{
                            max:40,
                            min:10
                        },
                        
                       
                    }
                     },
                this.viz = new NeoVis.default(newConfig)
                this.viz.render() // 渲染
                loading.close()
               
               
    },
            choose(choice){
                this.choice=choice
            //   this.sentence='MATCH p=(n:'+choice+')-[]-() RETURN p limit 300'
              this.sentence="MATCH p=(n:`"
                            +choice
                            +"`{theme:'"
                            +this.input
                            +"'})-[]-(m:`"
                            +choice
                            +"`{theme:'"
                            +this.input
                            +"'}) RETURN p limit 200"
            //   console.log(this.sentence)
              this.draw ()

            },
            change(value){
                if (this.choice!='')
                    this.draw()
            },
            async get_keyword(){
                const {data:res} = await this.$axios.get('get_keyword/')
                this.option_key = []
                for (let i=0; i < res.data.length; i++) {
                    this.option_key.push({'value':res.data[i]})
                }
                // console.log(res)
                // console.log(this.option_key)
            },
            drawt(){
                if (this.choice!='')
                    this.draw()
            }

            
        },
        
    }
    
</script>

<style lang="less" scoped>
/deep/ .el-button {
    background-color: transparent;
  }

</style>