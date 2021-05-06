import com.alibaba.fastjson.JSONObject
import org.jsoup.Connection
import org.jsoup.Jsoup
import org.jsoup.nodes.Document

class YsuNetLogin {

    //初始化状态检查
    private var alreadyCheckedAuthStatus = false

    //    0.校园网 1.中国移动 2.中国联通 3.中国电信
    private val serviceCode = arrayOf(
            "%e6%a0%a1%e5%9b%ad%e7%bd%91",
            "%E4%B8%AD%E5%9B%BD%E7%A7%BB%E5%8A%A8",
            "%e4%b8%ad%e5%9b%bd%e8%81%94%e9%80%9a",
            "%e4%b8%ad%e5%9b%bd%e7%94%b5%e4%bf%a1"
    )

    private val userAgent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) " +
            "AppleWebKit/537.36 (KHTML, like Gecko) " +
            "Chrome/85.0.4183.83 Safari/537.36"

    private val url = "http://auth.ysu.edu.cn/eportal/InterFace.do?method="

    private var isAuth: Boolean = false

    private var userIndex: String = ""
    private var connectInfo: String = ""

    fun getAuthStatus(): Boolean {
        return try {
            val doc: Document = Jsoup.connect("http://auth.ysu.edu.cn").userAgent(userAgent).get()
            //    println(doc.baseUri())
            //    println(doc.location())
            this.isAuth = doc.baseUri().toString().indexOf("success.jsp") > -1
            this.alreadyCheckedAuthStatus = true
            this.isAuth
        } catch (e: Exception) {
            false
        }
    }

    fun login(user: String, pwd: String, type: Int, code: String?): Pair<Boolean, String> {
        try {
            val doc: Document = Jsoup.connect("http://auth.ysu.edu.cn").userAgent(userAgent).get()
            this.isAuth = doc.baseUri().toString().indexOf("success.jsp") > -1
            this.alreadyCheckedAuthStatus = true

            if (!(this.isAuth)) {
                if (user.isEmpty() || pwd.isEmpty()) {
                    return Pair(false, "用户名或密码为空")
                }

                //正则匹配queryString
                val queryString = Regex("""href='.*?\?(.*?)'""")
                        .findAll(doc.toString()).toList().flatMap(MatchResult::groupValues)

                val connect: Connection = Jsoup.connect(this.url + "login").userAgent(userAgent)

                connect.data("userId", user)
                connect.data("password", pwd)
                connect.data("service", serviceCode[type])
                connect.data("operatorPwd", "")
                connect.data("operatorUserId", "")
                connect.data("validcode", code)
                connect.data("passwordEncrypt", "False")
                connect.data("queryString", queryString[1])

                val document: Document = connect.post()

                val outJson = JSONObject.parseObject(getJson(document.body().toString()))
                this.userIndex = outJson.getString("userIndex")
                this.connectInfo = outJson.getString("message")
                val result = outJson.getString("result")

                return if (result == "success") {
                    Pair(true, "认证成功")
                } else {
                    Pair(false, this.connectInfo)
                }

            } else {
                return Pair(true, "已经在线")
            }

        } catch (e: Exception) {
            var msg = "Exception"
            if (e.message != null) {
                msg = e.message.toString()
            }

            return Pair(false, msg)
        }
    }

    class UserInfo constructor(json: String) {

        private var userName: String = ""
        private var userId: String = ""
        private var password: String = ""
        private var userGroup: String = ""
        private var userIp: String = ""
        private var userMac: String = ""
        private var portalIp: String = ""
        private var welcomeTip: String = ""

        init {
            var index = json.indexOf("<div")

            var repairJson = json.substring(0, index)

            index = json.lastIndexOf("</div>")
            repairJson = (repairJson + json.substring(index)).replace("\n", "")

            val outJson = JSONObject.parseObject(repairJson)

            val userName: String? = outJson.getString("userName")
            val userId: String? = outJson.getString("userId")
            val password: String? = outJson.getString("password")
            val userGroup: String? = outJson.getString("userGroup")
            val userIp: String? = outJson.getString("userIp")
            val userMac: String? = outJson.getString("userMac")
            val portalIp: String? = outJson.getString("portalIp")
            val welcomeTip: String? = outJson.getString("welcomeTip")

            if (userName != null) {
                this.userName = userName
            }

            if (userId != null) {
                this.userId = userId
            }

            if (password != null) {
                this.password = password
            }

            if (userGroup != null) {
                this.userGroup = userGroup
            }

            if (userIp != null) {
                this.userIp = userIp
            }

            if (userMac != null) {
                this.userMac = userMac
            }

            if (portalIp != null) {
                this.portalIp = portalIp
            }

            if (welcomeTip != null) {
                this.welcomeTip = welcomeTip
            }

        }

        fun getUserName(): String {
            return this.userName
        }

        fun getUserID(): String {
            return this.userId
        }

        fun getUserGroup(): String {
            return this.userGroup
        }

        fun getUserIP(): String {
            return this.userIp
        }

        fun getUserMAC(): String {
            return this.userMac
        }

        fun getPortalIP(): String {
            return this.portalIp
        }

        fun getWelcomeTip(): String {
            return this.welcomeTip
        }


    }

    fun getUserData(): UserInfo {
        val doc: Document =
                Jsoup.connect("http://auth.ysu.edu.cn/eportal/InterFace.do?method=getOnlineUserInfo")
                        .userAgent(userAgent).get()

        return UserInfo(getJson(doc.body().toString()))
    }

    fun logout(): Pair<Boolean, String> {
        return try {
            val doc: Document = Jsoup.connect(this.url + "logout").userAgent(userAgent).get()

            val outJson = JSONObject.parseObject(getJson(doc.toString()))

            this.connectInfo = outJson.getString("message")
            val result = outJson.getString("result")

            if (result == "success") {
                Pair(true, "下线成功")
            } else {
                Pair(false, this.connectInfo)
            }
        } catch (e: Exception) {
            var msg = "Exception"
            if (e.message != null) {
                msg = e.message.toString()
            }

            Pair(false, msg)
        }
    }

    fun isCampusNetwork(timeout: Int = 100): Boolean {
        return try {
            Jsoup.connect("http://auth.ysu.edu.cn").userAgent(userAgent).timeout(timeout).get()
            true
        } catch (e: Exception) {
            false
        }
    }

    private fun getJson(src: String): String {
        var r = src
        var index = r.indexOf("{")
        if (index > -1) {
            r = r.substring(index)
        }
        index = r.lastIndexOf("}")
        if (index > -1) {
            r = r.substring(0, index + 1)
        }

        return r
    }

}