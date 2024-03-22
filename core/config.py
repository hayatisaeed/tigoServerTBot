class BotData:
    botUsername = ""
    botFatherToken = ""


class AdminData:
    adminChatId = ""
    adminUsername = ""
    adminName = ""


class ChannelData:
    channelName = ""
    channelChatId = ""
    channelUsername = ""


class SellData:
    sellingIsAllowed = True

    def __init__(self):
        SellData.update_data()  # updates data at the beginning

    @classmethod
    def update_data(cls):
        # updates the sellingIsAllowed parameter from database

        updated_value_from_database = False  # I should replace it with database logic

        cls.sellingIsAllowed = updated_value_from_database


class PaymentGatewayData:
    gatewayProviderName = ""
    merchantId = ""
    newPaymentURL = ""
    minimumAmount = 0
    paymentCurrency = "Rials"
