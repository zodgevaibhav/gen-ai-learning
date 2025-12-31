| Sr. | Category               | Use Case                                         | Risk   |
| --- | ---------------------- | ------------------------------------------------ | ------ |
| 1   | Stolen Card            | Card used immediately after reported stolen      | High   |
| 2   | Stolen Card            | Multiple transactions in short time window       | High   |
| 3   | Stolen Card            | First transaction after long inactivity          | Medium |
| 4   | Stolen Card            | Transaction from unusual merchant                | Medium |
| 5   | Stolen Card            | Card used without CVV                            | High   |
| 6   | Stolen Card            | Offline transaction using stolen card            | High   |
| 7   | Stolen Card            | ATM + POS transactions back-to-back              | High   |
| 8   | Stolen Card            | Card used in different city within minutes       | High   |
| 9   | Stolen Card            | High-value purchase after theft                  | High   |
| 10  | Stolen Card            | Card swipe after customer travel alert not set   | Medium |
| 11  | Lost Card              | Card used before customer reports loss           | Medium |
| 12  | Lost Card              | Multiple small test transactions                 | High   |
| 13  | Lost Card              | First-ever international transaction             | High   |
| 14  | Lost Card              | Merchant category never used before              | Medium |
| 15  | Lost Card              | Declined transaction followed by success         | Medium |
| 16  | Lost Card              | Usage outside customer home location             | Medium |
| 17  | Lost Card              | Repeated declines due to PIN failure             | High   |
| 18  | Lost Card              | Tap-to-pay transactions without PIN              | Medium |
| 19  | Lost Card              | Unusual spending pattern                         | Medium |
| 20  | Lost Card              | Card used at odd hours                           | Low    |
| 21  | Card Not Present (CNP) | Online transaction without OTP                   | High   |
| 22  | CNP                    | Multiple e-commerce transactions quickly         | High   |
| 23  | CNP                    | High-risk MCC (electronics, gift cards)          | High   |
| 24  | CNP                    | Foreign IP address used                          | High   |
| 25  | CNP                    | Shipping and billing address mismatch            | High   |
| 26  | CNP                    | VPN or proxy detected                            | Medium |
| 27  | CNP                    | Repeated failed OTP attempts                     | High   |
| 28  | CNP                    | Transaction via new device/browser               | Medium |
| 29  | CNP                    | Subscription setup without prior history         | Medium |
| 30  | CNP                    | Merchant with high chargeback ratio              | High   |
| 31  | Identity Theft         | Card used after KYC change                       | High   |
| 32  | Identity Theft         | Email/phone changed before transaction           | High   |
| 33  | Identity Theft         | Password reset followed by payment               | High   |
| 34  | Identity Theft         | New address + transaction same day               | High   |
| 35  | Identity Theft         | Card used after SIM swap                         | High   |
| 36  | Identity Theft         | Account takeover indicators present              | High   |
| 37  | Identity Theft         | Multiple cards linked to same device             | High   |
| 38  | Identity Theft         | New beneficiary + payment                        | High   |
| 39  | Identity Theft         | Change in spending geography                     | Medium |
| 40  | Identity Theft         | First digital wallet tokenization                | Medium |
| 41  | Friendly Fraud         | Customer disputes genuine transaction            | Medium |
| 42  | Friendly Fraud         | Family member misuse                             | Low    |
| 43  | Friendly Fraud         | Subscription forgotten by customer               | Low    |
| 44  | Friendly Fraud         | Chargeback after delivery confirmation           | Medium |
| 45  | Friendly Fraud         | Duplicate dispute attempts                       | Medium |
| 46  | Merchant Fraud         | Merchant inflating transaction amount            | High   |
| 47  | Merchant Fraud         | Hidden recurring charges                         | High   |
| 48  | Merchant Fraud         | Split transactions to bypass limits              | High   |
| 49  | Merchant Fraud         | Fake refund scams                                | High   |
| 50  | Merchant Fraud         | Excessive manual key-in transactions             | High   |
| 51  | Cross-Border           | International transaction without travel history | High   |
| 52  | Cross-Border           | High-risk country transaction                    | High   |
| 53  | Cross-Border           | Multiple countries in one day                    | High   |
| 54  | Cross-Border           | Currency mismatch behavior                       | Medium |
| 55  | Cross-Border           | Merchant country ≠ IP country                    | High   |
| 56  | Velocity               | Multiple transactions in seconds                 | High   |
| 57  | Velocity               | Rapid retries after decline                      | High   |
| 58  | Velocity               | Same amount repeated many times                  | High   |
| 59  | Velocity               | Spending spike vs average                        | Medium |
| 60  | Velocity               | Midnight transaction burst                       | Medium |
| 61  | Digital Wallet         | New wallet added and used instantly              | High   |
| 62  | Digital Wallet         | Wallet used without biometric                    | Medium |
| 63  | Digital Wallet         | Wallet used on jailbroken/rooted device          | High   |
| 64  | Digital Wallet         | Tokenized card used internationally              | Medium |
| 65  | Digital Wallet         | Multiple wallets linked to same card             | High   |
| 66  | ATM Fraud              | Skimming pattern detected                        | High   |
| 67  | ATM Fraud              | Unusual withdrawal location                      | Medium |
| 68  | ATM Fraud              | Consecutive max-limit withdrawals                | High   |
| 69  | ATM Fraud              | Withdrawal after failed POS txn                  | Medium |
| 70  | ATM Fraud              | Withdrawal in high-fraud zone                    | High   |
| 71  | BIN Attack             | Sequential card number attempts                  | High   |
| 72  | BIN Attack             | Multiple cards attacked at same merchant         | High   |
| 73  | BIN Attack             | Low-value test charges                           | High   |
| 74  | BIN Attack             | CVV brute-force attempts                         | High   |
| 75  | BIN Attack             | Expiry date guessing pattern                     | High   |
| 76  | Malware                | Infected device detected                         | High   |
| 77  | Malware                | Screen overlay attack pattern                    | High   |
| 78  | Malware                | Keylogger indicators present                     | High   |
| 79  | Malware                | Suspicious background app usage                  | Medium |
| 80  | Malware                | Remote access tool detected                      | High   |
| 81  | Refund Abuse           | Refund to different card                         | High   |
| 82  | Refund Abuse           | Excessive refunds requested                      | Medium |
| 83  | Refund Abuse           | Refund without original sale                     | High   |
| 84  | Refund Abuse           | Refund immediately after purchase                | Medium |
| 85  | Refund Abuse           | Partial refund manipulation                      | Medium |
| 86  | Behavioral             | Spending outside salary cycle                    | Medium |
| 87  | Behavioral             | Unusual MCC combinations                         | Medium |
| 88  | Behavioral             | Card used while customer inactive on app         | Medium |
| 89  | Behavioral             | Transaction deviates from peer group             | Medium |
| 90  | Behavioral             | Change in merchant visit frequency               | Low    |
| 91  | Contactless            | Tap payments without prior usage                 | Medium |
| 92  | Contactless            | Multiple tap txns under PIN limit                | High   |
| 93  | Contactless            | Offline tap transactions                         | High   |
| 94  | Contactless            | Transit fraud pattern                            | Medium |
| 95  | Contactless            | Same terminal repeated usage                     | Medium |
| 96  | Subscription Fraud     | Trial converted without consent                  | Medium |
| 97  | Subscription Fraud     | Multiple subscriptions in a day                  | Medium |
| 98  | Subscription Fraud     | Subscription cancellation blocked                | Medium |
| 99  | Synthetic Identity     | New card + high spend immediately                | High   |
| 100 | Synthetic Identity     | Thin-file customer abnormal activity             | High   |
