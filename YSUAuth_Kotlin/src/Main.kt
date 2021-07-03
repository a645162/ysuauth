import org.jsoup.Jsoup
import org.jsoup.nodes.Document
import java.net.UnknownHostException

private val userAgent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) " +
        "AppleWebKit/537.36 (KHTML, like Gecko) " +
        "Chrome/85.0.4183.83 Safari/537.36"

fun main() {
//    print("Test")

    val ysuNetLogin = YsuNetLogin()
    println(ysuNetLogin.getAuthStatus())
//    println(ysuNetLogin.logout())
//    println(ysuNetLogin.getAuthStatus())

    //TODO:还是有问题！
    println(ysuNetLogin.isCampusNetwork())


//    val userInfo = ysuNetLogin.getUserData()
//    println(userInfo.getUserName())

}
