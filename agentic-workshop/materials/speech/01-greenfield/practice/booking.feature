Feature: 核心訂票
  @AC-G-005 @AC-G-009
  Scenario: 成人與學生一起訂票
    Given 狀態已重置，T001基本票價700且剩餘20座
    When 為T001建立一位成人與一位學生的訂票
    Then 訂票總額為1225且為整數
    And 訂票狀態為PENDING_PAYMENT
    And T001剩餘18座

  @AC-G-006 @AC-G-007
  Scenario Outline: 驗證旅客人數
    Given 狀態已重置，T001剩餘20座
    When 為T001建立<count>位成人的訂票
    Then 建立結果為<result>
    And 剩餘座位為<seats>
    And 新增Booking筆數為<bookings>
    Examples:
      | count | result | seats | bookings |
      | 0     | 拒絕   | 20    | 0        |
      | 4     | 成功   | 16    | 1        |
      | 5     | 拒絕   | 20    | 0        |

  @AC-G-008
  Scenario: 容量不足不留下部分交易
    Given 狀態已重置，T001剩餘1座
    When 為T001建立2位成人的訂票
    Then 訂票被拒絕
    And T001仍剩餘1座
    And 不新增Booking

  @AC-G-010
  Scenario: 成功付款建立唯一訂單
    Given 狀態已重置，已有T001成人與學生總額1225的待付款訂票
    And 模擬付款結果設定為成功
    When 為該訂票付款
    Then Booking狀態為PAID
    And 建立唯一Order且金額1225

  @AC-G-011
  Scenario: 重複付款不新增訂單
    Given 狀態已重置，已有已付款Booking及其唯一Order
    When 再次為該Booking付款
    Then 付款被拒絕
    And Order仍只有一筆

  @AC-G-014
  Scenario: 付款失敗保持待付款
    Given 狀態已重置，已有T001一位成人的待付款訂票且剩餘19座
    And 模擬付款結果設定為失敗
    When 為該訂票付款
    Then 不建立Order
    And Booking仍為PENDING_PAYMENT
    And T001仍剩餘19座
