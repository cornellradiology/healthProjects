
import Foundation
import UIKit
import Alamofire

enum Router{
    static let baseURLString = "http:/192.168.1.13:54321/api"
    static var token = NSUserDefaults.standardUserDefaults().stringForKey("token")
    static let id = NSUserDefaults.standardUserDefaults().stringForKey("id")
}

class Network {
    
    class func getHeader() -> [String: String] {
        let plainString = Router.token! + ": "
        let plainData = plainString.dataUsingEncoding(NSUTF8StringEncoding)
        let base64String = plainData?.base64EncodedStringWithOptions(NSDataBase64EncodingOptions(rawValue: 0))
        return ["Authorization": "Basic " + base64String!]
    }

    class func sendData(data: [String: AnyObject], completionHandler:((Bool)->Void)) {
        Alamofire.request(.POST,
            Router.baseURLString + "/senddata",
            headers: Network.getHeader(),
            parameters: data,
            encoding: .JSON)
            .responseJSON{ resp in
                if let j = resp.2.value as? [String:AnyObject] {
                    let str = j["success"] as! String
                    var b = (str == "1")
                    completionHandler(b)
                }
            }
    }
    
    class func login(email: String, pwd: String) -> Bool? {
        let monitor = TRVSMonitor()
        let para = ["email": email, "pwd": pwd]
        var result = false
        Alamofire.request(.POST,
            Router.baseURLString + "/user/login",
            parameters: para,
            encoding: .JSON)
            .responseJSON { resp  in
                if let j = resp.2.value as? [String: AnyObject] {
                    let defaults = NSUserDefaults.standardUserDefaults()
                    let token = j["token"] as? String
                    if (token != nil) {
                        defaults.setObject(token, forKey: "token")
                        Router.token = token
                        result = true
                    }
                    monitor.signal()
                }
        }
        monitor.wait()
        return result
    }
    
    class func register(email: String, pwd: String) -> Bool? {
        let para = ["email": email, "pwd": pwd]
        let monitor = TRVSMonitor()
        var result: Bool?
        Alamofire.request(.POST,
            Router.baseURLString + "/user/register",
            parameters:para,
            encoding:.JSON)
            .responseJSON { resp  in
                if let j = resp.2.value as? [String: AnyObject] {
                    let defaults = NSUserDefaults.standardUserDefaults()
                    let token = j["token"] as? String
                    if (token != nil) {
                        defaults.setObject(token, forKey: "token")
                        Router.token = token
                        result = true
                    }
                    else {
                        result = false
                    }
                    monitor.signal()
                }
        }
        monitor.wait()
        return result
    }
    
}
