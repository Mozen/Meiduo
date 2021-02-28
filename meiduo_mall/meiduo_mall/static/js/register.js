let vm = new Vue({
	el: '#app', // 通过ID选择器找到绑定的HTML内容
	// 修改Vue读取变量的语法
    delimiters: ['[[', ']]'],
	data: {  //数据对象
        //v-model
		username: '',		// 用户名
		password: '', 		// 密码
		password2: '',		// 确认密码
		mobile: '',			// 手机号
		allow: '',			// 同意协议
        image_code_url:'', // 图像验证url
        uuid:'',            // uuid
        image_code:'',
		sms_code_tip: '获取短信验证码',
        sms_locked:false,
        sms_code:'',

        // v-show
		error_name: false,
		error_password: false,
		error_password2: false,
		error_mobile: false,
		error_allow: false,
        error_image_code :false,
        error_sms_code :false,


		error_name_message: '',		// 用户名错误提示
		error_mobile_message: '',	// 密码错误提示
        error_image_code_message:'',
        error_sms_code_message:''
	},

    mounted(){  //页面加载完会调用
	    // 生成图像验证码
        this.generate_image_code();
    },

	methods: {  //定义和实现事件方法
		//发送短信验证码
		// axios.get('url','请求头')
        send_sms_code() {
            // 给短信验证码加锁， 防治恶意点击
            if (this.sms_locked == true){
                return;
            }
            this.sms_locked = true;

            // 验证 mobile 和 image_code的有效性
            this.check_mobile();
            this.check_image_code();

            if ( this.error_mobile || this.error_image_code){
                this.sms_locked = false;
                return;
            }

            let url = '/sms_code/' + this.mobile + '/?image_code=' + this.image_code + '&uuid=' + this.uuid;
            axios.get(url, {
                responseType:'json'}
                )
                .then(response =>{
                        if (response.data.code == '0') {
                        // 展示倒计时60秒效果
                        let num = 60;
                        let t = setInterval(() => {
                            if (num == 1) { // 倒计时即将结束
                                clearInterval(t); // 停止回调函数的执行
                                this.sms_code_tip = '获取短信验证码'; // 还原sms_code_tip的提示文字
                                this.generate_image_code(); // 重新生成图形验证码
                                this.send_flag = false;
                                this.sms_locked = false;
                            } else { // 正在倒计时
                                num -= 1; // num = num - 1;
                                this.sms_code_tip = num + '秒';
                            }
                        }, 1000)
                        }else{
                            if (response.data.code == '4001') {
                                this.error_image_code_message = response.data.errmsg;
                                this.error_image_code = true;
                                this.sms_locked = false;
                            }else{
                                if (response.data.code == '4002'){
                                    this.error_sms_code_message = response.data.errmsg;
                                    this.error_sms_code = true;
                                    this.sms_locked = false;
                                }
                            }
                            this.send_flag = false;
                        }
                    })
                .catch(error => {
                    console.log('22222',error.response);
                    this.send_flag = false;
                    this.sms_locked = false;
                })
        },

        // 生成图形验证码的方法:封装的思想,代码复用
		generate_image_code(){
            this.uuid = generateUUID();
            this.image_code_url = '/image_code/' + this.uuid + '/';
         },

		// 校验用户名
		check_username(){
			// 准备正则表达式
            let re = /^[a-zA-Z0-9_-]{5,20}$/;
			// 正则表达式匹配用户名
			if (re.test(this.username)) {
				this.error_name = false;
			} else {
				this.error_name_message = '请输入5-20个字符的用户名';
				this.error_name = true;
			}

			// 判断用户名是否重复注册
            if (this.error_name == false) { // 只有当用户输入的用户名满足条件时才回去判断
                let url = '/username/' + this.username + '/count/';
                axios.get(url)
                    .then(response => {
                        console.log('*****',response);
                        if (response.data.count == 1) {
                            // 用户名已存在
                            this.error_name_message = '用户名已存在';
                            this.error_name = true;
                        } else {
                            // 用户名不存在
                            this.error_name = false;
                        }
                    })
                    .catch(error => {
                        console.log(444,error);
                    })
            }

		},
		// 校验密码
		check_password(){
			let re = /^[0-9A-Za-z]{8,20}$/;
			if (re.test(this.password)) {
				this.error_password = false;
			} else {
				this.error_password = true;
			}
		},
		// 校验确认密码
		check_password2(){
			// 判断两次密码是否一致
			if(this.password != this.password2) {
				this.error_password2 = true;
			} else {
				this.error_password2 = false;
			}
		},
		// 校验手机号
		check_mobile(){
			let re = /^1[3-9]\d{9}$/;
			if(re.test(this.mobile)) {
				this.error_mobile = false;
			} else {
				this.error_mobile_message = '您输入的手机号格式不正确';
				this.error_mobile = true;
			}
			if( this.error_mobile == false){
			    let url = '/mobile/' + this.mobile + '/count/';
			    axios.get(url)
                    .then(response => {
                        if (response.data.count == 1){
                            this.error_mobile_message = '您输入的手机号码已存在';
				            this.error_mobile = true;
                        }
                        else{
                            this.error_mobile = false;
                        }
                    })
                    .catch(error => {
                        console.log(error.repsonse)
                    })
            }
		},
        // 校验图形验证码吗
        check_image_code() {
            if (this.image_code.length != 4) {
                this.error_image_code_message = '请输入图形验证码';
                this.error_image_code = true;
            } else {
                this.error_image_code = false;
            }
        },

        // 校验短信验证码
        check_sms_code() {
            if (this.sms_code.length != 6) {
                this.error_sms_code_message = '请输入短信验证码';
                this.error_sms_code = true;
            } else {
                this.error_sms_code = false;
            }
        },

		// 校验是否勾选协议
		check_allow(){
			if(!this.allow) {
				this.error_allow = true;
			} else {
				this.error_allow = false;
			}
		},
		// 监听表单提交事件
		on_submit(){
			this.check_username();
			this.check_password();
			this.check_password2();
			this.check_mobile();
			this.check_allow();
			this.check_sms_code();

			if(this.error_name == true || this.error_password == true || this.error_password2 == true
				|| this.error_mobile == true || this.error_allow == true || this.error_sms_code == true) {
                // 禁用表单的提交
				window.event.returnValue = false;
            }
		},
	}
});