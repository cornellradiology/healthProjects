//
//  HealthProject_iOSTests.swift
//  HealthProject-iOSTests
//
//  Created by Matt on 15/10/2.
//  Copyright © 2015年 Weill.Cornell. All rights reserved.
//

import XCTest
@testable import HealthProject_iOS

class HealthProject_iOSTests: XCTestCase {
    let email = "abc@cornell.edu"
    let pwd = "pwd"
    
    override func setUp() {
        super.setUp()
    }
    
    override func tearDown() {
        super.tearDown()
        Network.delete(email)
    }
    
    func testExample() {
        let monitor = TRVSMonitor(expectedSignalCount: 1)
        XCTAssert(Network.register(email, pwd: pwd))
        Network.sendData(["test1":"test1"], completionHandler: {(success: Bool) in
            XCTAssert(success)
            monitor.signal()
            })
        XCTAssertFalse(Network.login(email + "test", pwd: pwd))
        XCTAssert(Network.login(email, pwd: pwd))
        Network.sendData(["test2":"test2"], completionHandler: {(success: Bool) in
            XCTAssert(success)
            monitor.signal()
            })
        monitor.wait()
    }
}
