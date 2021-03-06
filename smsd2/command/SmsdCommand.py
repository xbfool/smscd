from ChannelCommand import *
from UserCommand import *
from smsd2.command.Command import Command
from smsd2.command.Channel import ChannelItemController, ChannelListController
from smsd2.command.User import UserController
from CardCommand import *


class SmsdCommand(Command):
    def __init__(self, context):
        Command.__init__(self,
                         context,
                         no_command_callback  = self.__none_method_callback__, 
                         command_error_callback = self.__method_error_callback__)
        self.context.set_controller(
                                    channel_item = ChannelItemController(self.context),
                                    channel_list = ChannelListController(self.context),
                                    user = UserController(self.context),
                                    )
        command_list = [channel_item_add,
                        channel_item_del,
                        channel_item_update,
                        channel_item_query_by_uid,
                        channel_item_query_by_name,
                        channel_item_query_all,
                        channel_list_add,
                        channel_list_del,
                        channel_list_update,
                        channel_list_query_by_uid,
                        channel_list_query_by_name,
                        channel_list_query_all,
                        user_login,
                        user_query_all,
                        user_update_channel_list,
                        user_update_upload_url,
                        card_item_add,
                        card_item_delete,
                        card_item_query,
                        card_item_update,
                        card_item_add_list
                        ]
                        
        self.add_all(*command_list)
    
    def __none_method_callback__(self, context, param):
        return {'errno':-1001, 'errtext':'no such method', 'param': param}
    
    def __method_error_callback__(self, context, param):
        return {'errno':-1000, 'errtext':'method exec error', 'param': param}

