<template>
    <div id="content" class="col-md-12" style="margin-top: 30px; " >
        <el-row :gutter="20" style=" margin-right:250px">
            <el-col :span="6" :offset="6" >
                <el-select v-model="input" filterable placeholder="选择关键词" @change="getcountry()">
                    <el-option
                      v-for="item in option_key"
                      :key="item.value"
                      :value="item.value">
                    </el-option>
                </el-select>
               <!-- <el-input placeholder="请选择关键词主题" id="key" v-model="input">
                <el-button slot="append" icon="el-icon-search" @click="getcountry" ></el-button>
                </el-input> -->
             
            </el-col>
            
            <el-col :span="4">
                <el-button  @click="dialogTableVisible = true" icon="el-icon-more-outline">选择国家/地区</el-button>
                <el-dialog title="选择更多国家/地区(上限为10)" :visible.sync="dialogTableVisible">
                    <center><el-button  @click="add" icon="el-icon-plus" >添加</el-button></center>
                    <el-table :data="data">
                        <el-table-column 
                        fixed="right" 
                       label="删除">
                        <template  slot-scope="scope">
                       <el-button @click="deleteRow(scope.$index)" icon="el-icon-minus">删除</el-button>
                        </template>
                      </el-table-column>
                        <el-table-column label="操作" >
                        <template slot-scope="scope">
                            <el-select v-if="scope.$index==0" v-model="country0"  filterable placeholder="选择国家/地区" >
                                <el-option
                                  v-for="item in options"
                                  :key="item.value"
                                  :value="item.value">
                                </el-option>
                            </el-select>
                            <el-select v-if="scope.$index==1" v-model="country1"  filterable placeholder="选择国家/地区" >
                                <el-option
                                  v-for="item in options"
                                  :key="item.value"
                                  :value="item.value">
                                </el-option>
                            </el-select>
                            <el-select v-if="scope.$index==2" v-model="country2"  filterable placeholder="选择国家/地区" >
                                <el-option
                                  v-for="item in options"
                                  :key="item.value"
                                  :value="item.value">
                                </el-option>
                            </el-select>
                            <el-select v-if="scope.$index==3" v-model="country3"  filterable placeholder="选择国家/地区" >
                                <el-option
                                  v-for="item in options"
                                  :key="item.value"
                                  :value="item.value">
                                </el-option>
                            </el-select>
                            <el-select v-if="scope.$index==4" v-model="country4"  filterable placeholder="选择国家/地区" >
                                <el-option
                                  v-for="item in options"
                                  :key="item.value"
                                  :value="item.value">
                                </el-option>
                            </el-select>
                            <el-select v-if="scope.$index==5" v-model="country5"  filterable placeholder="选择国家/地区" >
                                <el-option
                                  v-for="item in options"
                                  :key="item.value"
                                  :value="item.value">
                                </el-option>
                            </el-select>
                            <el-select v-if="scope.$index==6" v-model="country6"  filterable placeholder="选择国家/地区" >
                                <el-option
                                  v-for="item in options"
                                  :key="item.value"
                                  :value="item.value">
                                </el-option>
                            </el-select>
                            <el-select v-if="scope.$index==7" v-model="country7"  filterable placeholder="选择国家/地区" >
                                <el-option
                                  v-for="item in options"
                                  :key="item.value"
                                  :value="item.value">
                                </el-option>
                            </el-select>
                            <el-select v-if="scope.$index==8" v-model="country8"  filterable placeholder="选择国家/地区" >
                                <el-option
                                  v-for="item in options"
                                  :key="item.value"
                                  :value="item.value">
                                </el-option>
                            </el-select>
                            <el-select v-if="scope.$index==9" v-model="country9"  filterable placeholder="选择国家/地区" >
                                <el-option
                                  v-for="item in options"
                                  :key="item.value"
                                  :value="item.value">
                                </el-option>
                            </el-select>
                          
                          
                        </template>
                      </el-table-column>
                      
                  
                
                    </el-table>
                    </el-dialog>

            </el-col>
                   
       
           
            <el-col :span="3">
                <el-button  icon="el-icon-picture" @click="drawcountry">绘制</el-button>
            </el-col>
         

           
           
           
         
            
        </el-row>
        
    <section  class="tile transparent" style=" margin-right:250px;margin-top: 30px;"  >
        <div class="tile-widget color transparent-black textured">
            <div class="table-responsive" align="center">
                
                <div id="chart_lz_region" style="width: 100%; height: 600px;">
                    国家/地区合作图
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
                data:[],
                choice:'country',
                sentence:'',
                dialogTableVisible : false,
                input:'',
                options :[],
                country0:'',
                country1:'',
                country2:'',
                country3:'',
                country4:'',
                country5:'',
                country6:'',
                country7:'',
                country8:'',
                country9:'',
                sentence0:'',
                sentence1:'',
                sentence2:'',
                sentence3:'',
                sentence4:'',
                sentence5:'',
                sentence6:'',
                sentence7:'',
                sentence8:'',
                sentence9:'',
                
                option_key:[],
                
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
                    server_url: neourl, //连接的地址是端口号为7687的不是7474
                    server_user: 'neo4j',
                    server_password: '58094894',
                    // labels是节点样式的配置
                    // 没有在这个地方配置的节点将会是默认样式
                    
                    labels: {
                        'authorcooperate': {
                        
                            caption: 'name',  
                            // community: 'group1',
                            color: "lightblue",
                            size: 'number', 
                           
                        
                        },
                        'countrycooperate': {
                        
                            caption: 'name', 
                            // community: 'group2',
                            size: 'number', 

                        },
                        'institutioncooperate': {
                        
                            caption: 'name',  
                            // community: 'group3',
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
                // console.log(newConfig.labels.authorcooperate["value"])
                // console.log(newConfig.labels.authorcooperate[NeoVis.NEOVIS_ADVANCED_CONFIG])
                newConfig.labels.authorcooperate[NeoVis.NEOVIS_ADVANCED_CONFIG].static['color'] = '#90EE90'
                newConfig.labels.countrycooperate[NeoVis.NEOVIS_ADVANCED_CONFIG].static['color'] = '#1E90FF'
                newConfig.labels.institutioncooperate[NeoVis.NEOVIS_ADVANCED_CONFIG].static['color'] = '#FFA07A'
                // console.log(newConfig)
                
                newConfig.visConfig =  {
                    edges: {
                        arrows: {
                            to: {enabled: false}
                        },
                        //color:this.color2
                    },
                    nodes: {
                        shape: 'dot',
                        // color: '#000000',
                        scaling:{
                            max:40,
                            min:10
                        },
                        
                       
                    },
                    
                    
                     },
                this.viz = new NeoVis.default(newConfig)
                this.viz.render() // 渲染
                loading.close()
                
               
               
         },
            drawcountry(){
                this.sentence=''
                if(this.country0!=''){
                this.sentence+="MATCH p=(n:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country0+"'})-[]-(m:`institutioncooperate`{theme:'"
                + this.input+"'}) RETURN p UNION ALL"
                +" MATCH p=(n:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country0+"'})-[]-(m:`authorcooperate`{theme:'"
                + this.input+"'}) RETURN p"
                }
                if(this.country1!=''){
                this.sentence+=" UNION ALL MATCH p=(n:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country1+"'})-[]-(m:`institutioncooperate`{theme:'"
                + this.input+"'}) RETURN p UNION ALL"
                +" MATCH p=(n:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country1+"'})-[]-(m:`authorcooperate`{theme:'"
                + this.input+"'}) RETURN p UNION ALL"
                +" MATCH p=(n:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country0+"'})-[]-(m:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country1+"'}) RETURN p"
                }
                if(this.country2!=''){
                    this.sentence+=" UNION ALL MATCH p=(n:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country2+"'})-[]-(m:`institutioncooperate`{theme:'"
                + this.input+"'}) RETURN p UNION ALL"
                +" MATCH p=(n:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country2+"'})-[]-(m:`authorcooperate`{theme:'"
                + this.input+"'}) RETURN p UNION ALL"
                +" MATCH p=(n:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country0+"'})-[]-(m:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country2+"'}) RETURN p"
                +" UNION ALL MATCH p=(n:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country1+"'})-[]-(m:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country2+"'}) RETURN p"

                }
                if(this.country3!=''){
                    this.sentence+=" UNION ALL MATCH p=(n:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country3+"'})-[]-(m:`institutioncooperate`{theme:'"
                + this.input+"'}) RETURN p UNION ALL"
                +" MATCH p=(n:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country3+"'})-[]-(m:`authorcooperate`{theme:'"
                + this.input+"'}) RETURN p UNION ALL"
                +" MATCH p=(n:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country0+"'})-[]-(m:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country3+"'}) RETURN p"
                +" UNION ALL MATCH p=(n:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country1+"'})-[]-(m:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country3+"'}) RETURN p"
                +" UNION ALL MATCH p=(n:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country2+"'})-[]-(m:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country3+"'}) RETURN p"
                }
                if(this.country4!=''){
                    this.sentence+=" UNION ALL MATCH p=(n:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country4+"'})-[]-(m:`institutioncooperate`{theme:'"
                + this.input+"'}) RETURN p UNION ALL"
                +" MATCH p=(n:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country4+"'})-[]-(m:`authorcooperate`{theme:'"
                + this.input+"'}) RETURN p UNION ALL"
                +" MATCH p=(n:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country0+"'})-[]-(m:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country4+"'}) RETURN p"
                +" UNION ALL MATCH p=(n:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country1+"'})-[]-(m:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country4+"'}) RETURN p"
                +" UNION ALL MATCH p=(n:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country2+"'})-[]-(m:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country4+"'}) RETURN p"
                +" UNION ALL MATCH p=(n:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country3+"'})-[]-(m:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country4+"'}) RETURN p"
                }
                if(this.country5!=''){
                    this.sentence+=" UNION ALL MATCH p=(n:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country5+"'})-[]-(m:`institutioncooperate`{theme:'"
                + this.input+"'}) RETURN p UNION ALL"
                +" MATCH p=(n:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country5+"'})-[]-(m:`authorcooperate`{theme:'"
                + this.input+"'}) RETURN p UNION ALL"
                +" MATCH p=(n:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country0+"'})-[]-(m:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country5+"'}) RETURN p"
                +" UNION ALL MATCH p=(n:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country1+"'})-[]-(m:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country5+"'}) RETURN p"
                +" UNION ALL MATCH p=(n:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country2+"'})-[]-(m:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country5+"'}) RETURN p"
                +" UNION ALL MATCH p=(n:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country3+"'})-[]-(m:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country5+"'}) RETURN p"
                +" UNION ALL MATCH p=(n:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country4+"'})-[]-(m:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country5+"'}) RETURN p"


                }
                if(this.country6!=''){
                    this.sentence+=" UNION ALL MATCH p=(n:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country6+"'})-[]-(m:`institutioncooperate`{theme:'"
                + this.input+"'}) RETURN p UNION ALL"
                +" MATCH p=(n:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country6+"'})-[]-(m:`authorcooperate`{theme:'"
                + this.input+"'}) RETURN p UNION ALL"
                +" MATCH p=(n:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country0+"'})-[]-(m:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country6+"'}) RETURN p"
                +" UNION ALL MATCH p=(n:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country1+"'})-[]-(m:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country6+"'}) RETURN p"
                +" UNION ALL MATCH p=(n:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country2+"'})-[]-(m:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country6+"'}) RETURN p"
                +" UNION ALL MATCH p=(n:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country3+"'})-[]-(m:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country6+"'}) RETURN p"
                +" UNION ALL MATCH p=(n:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country4+"'})-[]-(m:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country6+"'}) RETURN p"
                +" UNION ALL MATCH p=(n:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country5+"'})-[]-(m:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country6+"'}) RETURN p"


                }
                if(this.country7!=''){
                    this.sentence+=" UNION ALL MATCH p=(n:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country7+"'})-[]-(m:`institutioncooperate`{theme:'"
                + this.input+"'}) RETURN p UNION ALL"
                +" MATCH p=(n:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country7+"'})-[]-(m:`authorcooperate`{theme:'"
                + this.input+"'}) RETURN p UNION ALL"
                +" MATCH p=(n:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country0+"'})-[]-(m:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country7+"'}) RETURN p"
                +" UNION ALL MATCH p=(n:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country1+"'})-[]-(m:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country7+"'}) RETURN p"
                +" UNION ALL MATCH p=(n:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country2+"'})-[]-(m:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country7+"'}) RETURN p"
                +" UNION ALL MATCH p=(n:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country3+"'})-[]-(m:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country7+"'}) RETURN p"
                +" UNION ALL MATCH p=(n:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country4+"'})-[]-(m:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country7+"'}) RETURN p"
                +" UNION ALL MATCH p=(n:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country5+"'})-[]-(m:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country7+"'}) RETURN p"
                +" UNION ALL MATCH p=(n:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country6+"'})-[]-(m:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country7+"'}) RETURN p"


                }
                if(this.country8!=''){
                    this.sentence+=" UNION ALL MATCH p=(n:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country8+"'})-[]-(m:`institutioncooperate`{theme:'"
                + this.input+"'}) RETURN p UNION ALL"
                +" MATCH p=(n:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country8+"'})-[]-(m:`authorcooperate`{theme:'"
                + this.input+"'}) RETURN p UNION ALL"
                +" MATCH p=(n:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country0+"'})-[]-(m:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country8+"'}) RETURN p"
                +" UNION ALL MATCH p=(n:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country1+"'})-[]-(m:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country8+"'}) RETURN p"
                +" UNION ALL MATCH p=(n:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country2+"'})-[]-(m:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country8+"'}) RETURN p"
                +" UNION ALL MATCH p=(n:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country3+"'})-[]-(m:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country8+"'}) RETURN p"
                +" UNION ALL MATCH p=(n:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country4+"'})-[]-(m:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country8+"'}) RETURN p"
                +" UNION ALL MATCH p=(n:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country5+"'})-[]-(m:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country8+"'}) RETURN p"
                +" UNION ALL MATCH p=(n:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country6+"'})-[]-(m:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country8+"'}) RETURN p"
                +" UNION ALL MATCH p=(n:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country7+"'})-[]-(m:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country8+"'}) RETURN p"


                }
                if(this.country9 !=''){
                    this.sentence+=" UNION ALL MATCH p=(n:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country9+"'})-[]-(m:`institutioncooperate`{theme:'"
                + this.input+"'}) RETURN p UNION ALL"
                +" MATCH p=(n:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country9+"'})-[]-(m:`authorcooperate`{theme:'"
                + this.input+"'}) RETURN p UNION ALL"
                +" MATCH p=(n:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country0+"'})-[]-(m:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country9+"'}) RETURN p"
                +" UNION ALL MATCH p=(n:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country1+"'})-[]-(m:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country9+"'}) RETURN p"
                +" UNION ALL MATCH p=(n:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country2+"'})-[]-(m:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country9+"'}) RETURN p"
                +" UNION ALL MATCH p=(n:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country3+"'})-[]-(m:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country9+"'}) RETURN p"
                +" UNION ALL MATCH p=(n:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country4+"'})-[]-(m:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country9+"'}) RETURN p"
                +" UNION ALL MATCH p=(n:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country5+"'})-[]-(m:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country9+"'}) RETURN p"
                +" UNION ALL MATCH p=(n:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country6+"'})-[]-(m:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country9+"'}) RETURN p"
                +" UNION ALL MATCH p=(n:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country7+"'})-[]-(m:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country9+"'}) RETURN p"
                +" UNION ALL MATCH p=(n:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country8+"'})-[]-(m:`countrycooperate`{theme:'"
                +this.input+"',name:'"
                +this.country9+"'}) RETURN p"


                }
                // RETURN p"
                
               
              console.log(this.sentence)
              this.draw()

            },
           
            async getcountry(){
                
                const {data:res} = await this.$axios.get('get_country/',{params:{'key':this.input}})
                this.options = []
                for (let i=0; i < res.data.length; i++) {
                    this.options.push({'value':res.data[i]})
                }
                
                
            },
            async get_keyword(){
                const {data:res} = await this.$axios.get('get_keyword/')
                this.option_key = []
                for (let i=0; i < res.data.length; i++) {
                    this.option_key.push({'value':res.data[i]})
                }
               
            },
            add(){
                
                this.data.push({value:this.countrynum});
                
                
            },
            deleteRow(index){
            this.data.splice(index,1);
            },
            numToStr(num) {
            num = num.toString();
            return num;
            },


          

            
        },
        
    }
    
</script>

<style lang="less" scoped>
/deep/ .el-button {
    background-color: transparent;
  }

</style>