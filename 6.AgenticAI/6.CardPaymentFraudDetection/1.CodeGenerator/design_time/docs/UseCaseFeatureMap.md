| Category           | Use Case                          | Primary Feature             | Secondary Feature        | Criticality |
| ------------------ | --------------------------------- | --------------------------- | ------------------------ | ----------- |
| Stolen Card        | Card used immediately after theft | `time_since_block`          | `txn_velocity_5m`        | High        |
| Stolen Card        | Multiple transactions quickly     | `txn_count_5m`              | `same_amount_repeat`     | High        |
| Stolen Card        | New merchant usage                | `new_merchant_flag`         | `merchant_risk_score`    | Medium      |
| Stolen Card        | Offline transaction               | `offline_txn_flag`          | `entry_mode`             | High        |
| Stolen Card        | High value after inactivity       | `amount_spike_ratio`        | `avg_amount_30d`         | High        |
| Stolen Card        | Geo jump usage                    | `geo_distance_km`           | `time_gap`               | High        |
| Lost Card          | Small test transactions           | `low_amount_velocity`       | `txn_count_10m`          | High        |
| Lost Card          | First international txn           | `first_international_flag`  | `travel_history`         | High        |
| Lost Card          | Usage at odd hours                | `hour_of_day`               | `user_sleep_pattern`     | Medium      |
| Lost Card          | Repeated PIN failure              | `pin_fail_count`            | `atm_id_risk`            | High        |
| CNP Fraud          | OTP bypassed                      | `otp_result`                | `channel=CNP`            | High        |
| CNP Fraud          | Rapid ecommerce spend             | `txn_count_10m`             | `merchant_diversity`     | High        |
| CNP Fraud          | Billing ≠ shipping                | `address_mismatch_flag`     | `new_address_flag`       | High        |
| CNP Fraud          | VPN / proxy detected              | `vpn_detected`              | `asn_risk`               | High        |
| CNP Fraud          | New device/browser                | `new_device_flag`           | `device_trust_score`     | Medium      |
| CNP Fraud          | High-risk MCC usage               | `mcc_risk_score`            | `merchant_cb_rate`       | High        |
| Identity Theft     | SIM swap before txn               | `sim_swap_days`             | `otp_fail_rate`          | High        |
| Identity Theft     | Profile change + spend            | `profile_change_recency`    | `txn_after_change`       | High        |
| Identity Theft     | Password reset abuse              | `pwd_reset_flag`            | `new_device_flag`        | High        |
| Identity Theft     | New wallet + spend                | `wallet_age_minutes`        | `first_wallet_txn`       | High        |
| Identity Theft     | Multiple cards per device         | `device_card_count`         | `device_risk_score`      | High        |
| Velocity           | Burst transactions                | `txn_count_1m`              | `channel_type`           | High        |
| Velocity           | Retry after decline               | `decline_retry_count`       | `same_amount_repeat`     | High        |
| Velocity           | Midnight burst                    | `hour_of_day`               | `txn_density`            | Medium      |
| Velocity           | Same amount loop                  | `same_amount_count`         | `merchant_id`            | High        |
| Cross-Border       | First international usage         | `is_first_international`    | `travel_history`         | High        |
| Cross-Border       | High-risk country                 | `country_risk_score`        | `merchant_country`       | High        |
| Cross-Border       | Impossible travel                 | `geo_distance / time_gap`   | `last_txn_country`       | High        |
| Cross-Border       | IP ≠ merchant country             | `ip_country_mismatch`       | `proxy_flag`             | High        |
| Digital Wallet     | New wallet instant spend          | `wallet_age_minutes`        | `txn_amount`             | High        |
| Digital Wallet     | Jailbroken device                 | `device_compromised_flag`   | `wallet_type`            | High        |
| Digital Wallet     | Multiple wallets per card         | `wallets_per_card`          | `device_id`              | Medium      |
| Digital Wallet     | Wallet used abroad                | `wallet_country_mismatch`   | `geo_velocity`           | Medium      |
| ATM Fraud          | Skimming pattern                  | `atm_risk_score`            | `entry_mode=magstripe`   | High        |
| ATM Fraud          | Max limit withdrawals             | `withdrawal_ratio`          | `daily_withdrawal_count` | High        |
| ATM Fraud          | POS fail → ATM                    | `pos_decline_then_atm`      | `time_gap`               | Medium      |
| ATM Fraud          | High-risk ATM zone                | `atm_geo_risk`              | `usage_history`          | High        |
| BIN Attack         | Sequential PAN attempts           | `bin_txn_velocity`          | `merchant_id`            | High        |
| BIN Attack         | CVV brute force                   | `cvv_fail_rate`             | `same_bin_cards`         | High        |
| BIN Attack         | Expiry guessing                   | `expiry_fail_pattern`       | `low_amount_trials`      | High        |
| BIN Attack         | Test charges                      | `amount < threshold`        | `repeat_count`           | High        |
| Merchant Fraud     | Inflated amount                   | `merchant_amount_deviation` | `customer_avg_spend`     | High        |
| Merchant Fraud     | Split transactions                | `txn_split_pattern`         | `merchant_limit`         | High        |
| Merchant Fraud     | Fake refunds                      | `refund_without_sale`       | `refund_latency`         | High        |
| Merchant Fraud     | Manual key-in abuse               | `manual_entry_ratio`        | `merchant_risk_score`    | High        |
| Refund Abuse       | Refund to different card          | `refund_card_mismatch`      | `refund_velocity`        | High        |
| Refund Abuse       | Excessive refunds                 | `refund_ratio`              | `txn_count_30d`          | Medium      |
| Refund Abuse       | Instant refund after sale         | `refund_latency`            | `txn_amount`             | Medium      |
| Behavioral         | Spend outside salary cycle        | `salary_cycle_deviation`    | `monthly_pattern`        | Medium      |
| Behavioral         | Unusual MCC mix                   | `mcc_entropy`               | `peer_group_score`       | Medium      |
| Behavioral         | App inactive but card used        | `app_inactive_days`         | `txn_channel`            | Medium      |
| Behavioral         | Peer deviation                    | `peer_spend_zscore`         | `geo_pattern`            | Medium      |
| Contactless        | New tap usage                     | `first_contactless_flag`    | `txn_amount`             | Medium      |
| Contactless        | Multiple tap under limit          | `tap_velocity`              | `offline_flag`           | High        |
| Contactless        | Offline tap transactions          | `offline_contactless`       | `terminal_id`            | High        |
| Subscription Fraud | Trial auto-converted              | `trial_conversion_flag`     | `customer_history`       | Medium      |
| Subscription Fraud | Multiple subs/day                 | `subscription_velocity`     | `merchant_diversity`     | Medium      |
| Synthetic ID       | New card + high spend             | `card_age_days`             | `amount_spike_ratio`     | High        |
| Synthetic ID       | Thin-file abnormality             | `credit_history_length`     | `velocity_features`      | High        |
