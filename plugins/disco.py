#!/usr/bin/python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------- #
#                                                                             #
#    Plugin for iSida Jabber Bot                                              #
#    Copyright (C) diSabler <dsy@dsy.name>                                    #
#                                                                             #
#    This program is free software: you can redistribute it and/or modify     #
#    it under the terms of the GNU General Public License as published by     #
#    the Free Software Foundation, either version 3 of the License, or        #
#    (at your option) any later version.                                      #
#                                                                             #
#    This program is distributed in the hope that it will be useful,          #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of           #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            #
#    GNU General Public License for more details.                             #
#                                                                             #
#    You should have received a copy of the GNU General Public License        #
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.    #
#                                                                             #
# --------------------------------------------------------------------------- #

whereis_answers  = {}
whereis_regx     = re.compile('<item .*?name=[\'"](.*?)[\'"]',re.S|re.I|re.U)
whereis_lock     = None
disco_excl       = []

disco_features_list =  {'dnssrv':'Support for DNS SRV lookups of XMPP services., RFC 3920: XMPP Core, RFC 3921: XMPP IM',
						'fullunicode':'Support for Unicode characters, including in displayed text, JIDs, and passwords.',
						'gc-1.0':'Support for the "groupchat 1.0" protocol. (XEP-0045)',
						'http://jabber.org/protocol/activity':'User Activity (XEP-0108)',
						'http://jabber.org/protocol/address':'Extended Stanza Addressing (XEP-0033)',
						'http://jabber.org/protocol/amp':'Advanced Message Processing (XEP-0079)',
						'http://jabber.org/protocol/amp#errors':'Advanced Message Processing (XEP-0079)',
						'http://jabber.org/protocol/amp?action=alert':'Support for the "alert" action in Advanced Message Processing. (XEP-0079)',
						'http://jabber.org/protocol/amp?action=drop':'Support for the "drop" action in Advanced Message Processing. (XEP-0079)',
						'http://jabber.org/protocol/amp?action=error':'Support for the "error" action in Advanced Message Processing. (XEP-0079)',
						'http://jabber.org/protocol/amp?action=notify':'Support for the "notify" action in Advanced Message Processing. (XEP-0079)',
						'http://jabber.org/protocol/amp?condition=deliver':'Support for the "deliver" condition in Advanced Message Processing. (XEP-0079)',
						'http://jabber.org/protocol/amp?condition=expire-at':'Support for the "expire-at" condition in Advanced Message Processing. (XEP-0079)',
						'http://jabber.org/protocol/amp?condition=match-resource':'Support for the "match-resource" condition in Advanced Message Processing. (XEP-0079)',
						'http://jabber.org/protocol/bytestreams':'SOCKS5 Bytestreams (XEP-0065)',
						'http://jabber.org/protocol/bytestreams#udp':'SOCKS5 Bytestreams (XEP-0065)',
						'http://jabber.org/protocol/caps':'Entity Capabilities (XEP-0115)',
						'http://jabber.org/protocol/chatstates':'Chat State Notifications (XEP-0085)',
						'http://jabber.org/protocol/commands':'Ad-Hoc Commands (XEP-0050)',
						'http://jabber.org/protocol/compress':'Stream Compression (XEP-0138)',
						'http://jabber.org/protocol/disco#info':'Service Discovery Info (XEP-0030)',
						'http://jabber.org/protocol/disco#items':'Service Discovery Items (XEP-0030)',
						'http://jabber.org/protocol/feature-neg':'Feature Negotiation (XEP-0020)',
						'http://jabber.org/protocol/geoloc':'User Geolocation (XEP-0080)',
						'http://jabber.org/protocol/http-auth':'Verifying HTTP Requests via XMPP (XEP-0070)',
						'http://jabber.org/protocol/httpbind':'Bidirectional-streams Over Synchronous HTTP (XEP-0124)',
						'http://jabber.org/protocol/ibb':'In-Band Bytestreams (XEP-0047)',
						'http://jabber.org/protocol/mood':'User Mood (XEP-0107)',
						'http://jabber.org/protocol/muc':'Multi-User Chat (XEP-0045)',
						'http://jabber.org/protocol/muc#admin':'Multi-User Chat Admin (XEP-0045)',
						'http://jabber.org/protocol/muc#owner':'Multi-User Chat Owner (XEP-0045)',
						'http://jabber.org/protocol/muc#register':'Support for the muc#register FORM_TYPE in Multi-User Chat. (XEP-0045)',
						'http://jabber.org/protocol/muc#roomconfig':'Support for the muc#roomconfig FORM_TYPE in Multi-User Chat. (XEP-0045)',
						'http://jabber.org/protocol/muc#roominfo':'Support for the muc#roominfo FORM_TYPE in Multi-User Chat. (XEP-0045)',
						'http://jabber.org/protocol/muc#user':'Multi-User Chat User (XEP-0045)',
						'http://jabber.org/protocol/offline':'Flexible Offline Message Retrieval (XEP-0013)',
						'http://jabber.org/protocol/pubsub#access-authorize':'The default node access model is authorize. (XEP-0060)',
						'http://jabber.org/protocol/pubsub#access-open':'The default node access model is open. (XEP-0060)',
						'http://jabber.org/protocol/pubsub#access-presence':'The default node access model is presence. (XEP-0060)',
						'http://jabber.org/protocol/pubsub#access-roster':'The default node access model is roster. (XEP-0060)',
						'http://jabber.org/protocol/pubsub#access-whitelist':'The default node access model is whitelist. (XEP-0060)',
						'http://jabber.org/protocol/pubsub#auto-create':'The service supports automatic creation of nodes on first publish. (XEP-0060)',
						'http://jabber.org/protocol/pubsub#auto-subscribe':'The service supports automatic subscription to a nodes based on presence subscription. (XEP-0060)',
						'http://jabber.org/protocol/pubsub#collections':'Collection nodes are supported. (XEP-0060)',
						'http://jabber.org/protocol/pubsub#config-node':'Configuration of node options is supported. (XEP-0060)',
						'http://jabber.org/protocol/pubsub#create-and-configure':'Simultaneous creation and configuration of nodes is supported. (XEP-0060)',
						'http://jabber.org/protocol/pubsub#create-nodes':'Creation of nodes is supported. (XEP-0060)',
						'http://jabber.org/protocol/pubsub#delete-any':'Any publisher may delete an item (not only the originating publisher). (XEP-0060)',
						'http://jabber.org/protocol/pubsub#delete-nodes':'Deletion of nodes is supported. (XEP-0060)',
						'http://jabber.org/protocol/pubsub#filtered-notifications':'The service supports filtering of notifications based on Entity Capabilities. (XEP-0060)',
						'http://jabber.org/protocol/pubsub#get-pending':'Retrieval of pending subscription approvals is supported. (XEP-0060)',
						'http://jabber.org/protocol/pubsub#instant-nodes':'Creation of instant nodes is supported. (XEP-0060)',
						'http://jabber.org/protocol/pubsub#item-ids':'Publishers may specify item identifiers. (XEP-0060)',
						'http://jabber.org/protocol/pubsub#last-published':'The service supports sending of the last published item to new subscribers and to newly available resources. (XEP-0060)',
						'http://jabber.org/protocol/pubsub#leased-subscription':'Time-based subscriptions are supported. (XEP-0060)',
						'http://jabber.org/protocol/pubsub#manage-subscription':'Node owners may manage subscriptions. (XEP-0060)',
						'http://jabber.org/protocol/pubsub#member-affiliation':'The member affiliation is supported. (XEP-0060)',
						'http://jabber.org/protocol/pubsub#meta-data':'Node meta-data is supported. (XEP-0060)',
						'http://jabber.org/protocol/pubsub#modify-affiliations':'Node owners may modify affiliations. (XEP-0060)',
						'http://jabber.org/protocol/pubsub#multi-collection':'A single leaf node may be associated with multiple collections. (XEP-0060)',
						'http://jabber.org/protocol/pubsub#multi-subscribe':'A single entity may subscribe to a node multiple times. (XEP-0060)',
						'http://jabber.org/protocol/pubsub#outcast-affiliation':'The outcast affiliation is supported. (XEP-0060)',
						'http://jabber.org/protocol/pubsub#persistent-items':'Persistent items are supported. (XEP-0060)',
						'http://jabber.org/protocol/pubsub#presence-notifications':'Presence-based delivery of event notifications is supported. (XEP-0060)',
						'http://jabber.org/protocol/pubsub#presence-subscribe':'Implicit presence-based subscriptions are supported. (XEP-0060)',
						'http://jabber.org/protocol/pubsub#publish':'Publishing items is supported. (XEP-0060)',
						'http://jabber.org/protocol/pubsub#publish-options':'Publication with publish options is supported. (XEP-0060)',
						'http://jabber.org/protocol/pubsub#publisher-affiliation':'The publisher affiliation is supported. (XEP-0060)',
						'http://jabber.org/protocol/pubsub#purge-nodes':'Purging of nodes is supported. (XEP-0060)',
						'http://jabber.org/protocol/pubsub#retract-items':'Item retraction is supported. (XEP-0060)',
						'http://jabber.org/protocol/pubsub#retrieve-affiliations':'Retrieval of current affiliations is supported. (XEP-0060)',
						'http://jabber.org/protocol/pubsub#retrieve-default':'Retrieval of default node configuration is supported. (XEP-0060)',
						'http://jabber.org/protocol/pubsub#retrieve-items':'Item retrieval is supported. (XEP-0060)',
						'http://jabber.org/protocol/pubsub#retrieve-subscriptions':'Retrieval of current subscriptions is supported. (XEP-0060)',
						'http://jabber.org/protocol/pubsub#subscribe':'Subscribing and unsubscribing are supported. (XEP-0060)',
						'http://jabber.org/protocol/pubsub#subscription-options':'Configuration of subscription options is supported. (XEP-0060)',
						'http://jabber.org/protocol/pubsub#subscription-notifications':'Notification of subscription state changes is supported. (XEP-0060)',
						'http://jabber.org/protocol/rosterx':'Roster Item Exchange (XEP-0144)',
						'http://jabber.org/protocol/sipub':'Publishing SI Requests (XEP-0137)',
						'http://jabber.org/protocol/soap':'SOAP Over XMPP (XEP-0072)',
						'http://jabber.org/protocol/soap#fault':'SOAP Over XMPP (XEP-0072)',
						'http://jabber.org/protocol/waitinglist':'Waiting Lists (XEP-0130)',
						'http://jabber.org/protocol/waitinglist/schemes/mailto':'Waiting list service supports the mailto: URI scheme. (XEP-0130)',
						'http://jabber.org/protocol/waitinglist/schemes/tel':'Waiting list service supports the tel: URI scheme. (XEP-0130)',
						'http://jabber.org/protocol/xhtml-im':'XHTML-IM (XEP-0071)',
						'http://jabber.org/protocol/xdata-layout':'Data Forms Layout (XEP-0141)',
						'http://jabber.org/protocol/xdata-validate':'Data Forms Validation (XEP-0122)',
						'ipv6':'Application supports IPv6.',
						'jabber:client':'Client, XMPP IM (RFC 3921)',
						'jabber:component:accept':'Existing Component Protocol Accept(XEP-0114)',
						'jabber:component:connect':'Existing Component Protocol Connect (XEP-0114)',
						'jabber:iq:auth':'Non-SASL Authentication (XEP-0078)',
						'jabber:iq:browse':'Iq browse (XEP-0011, Deprecated)',
						'jabber:iq:gateway':'Gateway Interaction (XEP-0100)',
						'jabber:iq:last':'Last Activity (XEP-0012)',
						'jabber:iq:oob':'Out of Band Data (XEP-0066)',
						'jabber:iq:pass':'DEPRECATED (XEP-0003)',
						'jabber:iq:privacy':'Privacy Lists (XEP-0016) / XMPP IM (RFC 3921)',
						'jabber:iq:private':'Private XML Storage (XEP-0049)',
						'jabber:iq:register':'In-Band Registration (XEP-0077)',
						'jabber:iq:roster':'Roster, XMPP IM (RFC 3921)',
						'jabber:iq:rpc':'Jabber-RPC (XEP-0009)',
						'jabber:iq:search':'Jabber Search (XEP-0055)',
						'jabber:iq:version':'Software Version (XEP-0092)',
						'jabber:server':'Server, XMPP IM (RFC 3921)',
						'jabber:x:data':'Data Forms (XEP-0004)',
						'jabber:x:delay':'Delayed Delivery (XEP-0091, Deprecated)',
						'jabber:x:encrypted':'Current OpenPGP Usage (XEP-0027)',
						'jabber:x:event':'X:Event (XEP-0022, Deprecated)',
						'jabber:x:expire':'X:Expire (XEP-0023, Deprecated)',
						'jabber:x:oob':'Out of Band Data (XEP-0066)',
						'jabber:x:roster':'X:Roster (XEP-0093, Deprecated)',
						'jabber:x:signed':'Current OpenPGP Usage (XEP-0027)',
						'msglog':'Application performs logging or archiving of messages.',
						'msgoffline':'Server stores messages offline for later delivery. (XEP-0160)',
						'muc_hidden':'Hidden room in Multi-User Chat (MUC) (XEP-0045)',
						'muc_membersonly':'Members-only room in Multi-User Chat (MUC) (XEP-0045)',
						'muc_moderated':'Moderated room in Multi-User Chat (MUC) (XEP-0045)',
						'muc_nonanonymous':'Non-anonymous room in Multi-User Chat (MUC) (XEP-0045)',
						'muc_open':'Open room in Multi-User Chat (MUC) (XEP-0045)',
						'muc_passwordprotected':'Password-protected room in Multi-User Chat (MUC) (XEP-0045)',
						'muc_persistent':'Persistent room in Multi-User Chat (MUC) (XEP-0045)',
						'muc_public':'Public room in Multi-User Chat (MUC) (XEP-0045)',
						'muc_rooms':'List of MUC rooms (each as a separate item) (XEP-0045)',
						'muc_semianonymous':'Semi-anonymous room in Multi-User Chat (MUC) (XEP-0045)',
						'muc_temporary':'Temporary room in Multi-User Chat (MUC) (XEP-0045)',
						'muc_unmoderated':'Unmoderated room in Multi-User Chat (MUC) (XEP-0045)',
						'muc_unsecured':'Unsecured room in Multi-User Chat (MUC) (XEP-0045)',
						'roster:delimiter':'Nested Roster Groups (XEP-0083)',
						'sslc2s':'Application supports old-style (pre-TLS) SSL connections on a dedicated port.',
						'stringprep':'Application supports the nameprep, nodeprep, and resourceprep profiles of stringprep. (RFC 3920)',
						'urn:ietf:params:xml:ns:xmpp-bind':'XMPP Core Bind (RFC 3920)',
						'urn:ietf:params:xml:ns:xmpp-e2e':'XMPP E2E (RFC 3921)',
						'urn:ietf:params:xml:ns:xmpp-sasl':'XMPP Core Sasl (RFC 3920)',
						'urn:ietf:params:xml:ns:xmpp-sasl#c2s':'Application supports client-to-server SASL. (RFC 3920)',
						'urn:ietf:params:xml:ns:xmpp-sasl#s2s':'Application supports server-to-server SASL. (RFC 3920)',
						'urn:ietf:params:xml:ns:xmpp-session':'XMPP IM (RFC 3921)',
						'urn:ietf:params:xml:ns:xmpp-stanzas':'XMPP Core Stanzas (RFC 3920)',
						'urn:ietf:params:xml:ns:xmpp-streams':'XMPP Core Streams (RFC 3920)',
						'urn:ietf:params:xml:ns:xmpp-tls':'XMPP Core TLS (RFC 3920)',
						'urn:ietf:params:xml:ns:xmpp-tls#c2s':'Application supports client-to-server TLS. (RFC 3920)',
						'urn:ietf:params:xml:ns:xmpp-tls#s2s':'Application supports server-to-server TLS. (RFC 3920)',
						'urn:ietf:rfc:3264':'Jingle ICE-UDP Transport Method (XEP-0176)',
						'urn:xmpp:archive:auto':'Server supports automatic message archiving (XEP-0136)',
						'urn:xmpp:archive:manage':'Server supports management of archived messages (XEP-0136)',
						'urn:xmpp:archive:manual':'Server supports manual message archiving (XEP-0136)',
						'urn:xmpp:archive:pref':'Server supports message archiving preferences (XEP-0136)',
						'urn:xmpp:avatar:data':'User Avatars (XEP-0084)',
						'urn:xmpp:avatar:metadata':'User Avatars (XEP-0084)',
						'urn:xmpp:avatar:metadata+notify':'User Avatars and notify (XEP-0084)',
						'http://www.xmpp.org/extensions/xep-0084.html#ns-metadata+notify':'User Avatars and notify (XEP-0084)',
						'urn:xmpp:delay':'Delayed Delivery (XEP-0203)',
						'urn:xmpp:jingle:apps:rtp:audio':'Jingle RTP Sessions (XEP-0167)',
						'urn:xmpp:jingle:apps:rtp:video':'Jingle RTP Sessions (XEP-0167)',
						'urn:xmpp:ping':'XMPP Ping (XEP-0199)',
						'urn:xmpp:receipts':'Message Receipts (XEP-0184)',
						'urn:xmpp:ssn':'Support for Stanza Session Negotiation and its FORM_TYPE (XEP-0155)',
						'urn:xmpp:time':'Entity Time (XEP-0202)',
						'xmllang':'Application supports the \'xml:lang\' attribute as described in RFC 3920. (RFC 3920)',
						'vcard-temp':'vCard-temp (XEP-0054)',
						'http://jabber.org/protocol/admin':'Admin (XEP-0133)',
						'http://jabber.org/protocol/admin#add-user':'Add-user (XEP-0133)',
						'http://jabber.org/protocol/admin#delete-user':'Delete-user (XEP-0133)',
						'http://jabber.org/protocol/admin#disable-user':'Disable-user (XEP-0133)',
						'http://jabber.org/protocol/admin#reenable-user':'Reenable-user (XEP-0133)',
						'http://jabber.org/protocol/admin#end-user-session':'End-user-session (XEP-0133)',
						'http://jabber.org/protocol/admin#get-user-password':'Get-user-password (XEP-0133)',
						'http://jabber.org/protocol/admin#change-user-password':'Change-user-password (XEP-0133)',
						'http://jabber.org/protocol/admin#get-user-roster':'Get-user-roster (XEP-0133)',
						'http://jabber.org/protocol/admin#get-user-lastlogin':'Get-user-lastlogin (XEP-0133)',
						'http://jabber.org/protocol/admin#user-stats':'User-stats (XEP-0133)',
						'http://jabber.org/protocol/admin#edit-blacklist':'Edit-blacklist (XEP-0133)',
						'http://jabber.org/protocol/admin#edit-whitelist':'Edit-whitelist (XEP-0133)',
						'http://jabber.org/protocol/admin#get-registered-users-num':'Get-registered-users-num (XEP-0133)',
						'http://jabber.org/protocol/admin#get-disabled-users-num':'Get-disabled-users-num (XEP-0133)',
						'http://jabber.org/protocol/admin#get-online-users-num':'Get-online-users-num (XEP-0133)',
						'http://jabber.org/protocol/admin#get-active-users-num':'Get-active-users-num (XEP-0133)',
						'http://jabber.org/protocol/admin#get-idle-users-num':'Get-idle-users-num (XEP-0133)',
						'http://jabber.org/protocol/admin#get-registered-users-list':'Get-registered-users-list (XEP-0133)',
						'http://jabber.org/protocol/admin#get-disabled-users-list':'Get-disabled-users-list (XEP-0133)',
						'http://jabber.org/protocol/admin#get-online-users-list':'Get-online-users-list (XEP-0133)',
						'http://jabber.org/protocol/admin#get-active-users-list':'Get-active-users-list (XEP-0133)',
						'http://jabber.org/protocol/admin#get-idle-users-list':'Get-idle-users-list (XEP-0133)',
						'http://jabber.org/protocol/admin#announce':'Announce (XEP-0133)',
						'http://jabber.org/protocol/admin#set-motd':'Set-motd (XEP-0133)',
						'http://jabber.org/protocol/admin#edit-motd':'Edit-motd (XEP-0133)',
						'http://jabber.org/protocol/admin#delete-motd':'Delete-motd (XEP-0133)',
						'http://jabber.org/protocol/admin#set-welcome':'Set-welcome (XEP-0133)',
						'http://jabber.org/protocol/admin#delete-welcome':'Delete-welcome (XEP-0133)',
						'http://jabber.org/protocol/admin#edit-admin':'Edit-admin (XEP-0133)',
						'http://jabber.org/protocol/admin#restart':'Restart (XEP-0133)',
						'http://jabber.org/protocol/admin#shutdown':'Shutdown (XEP-0133)',
						'jabber:iq:agents':'Agents (XEP-0094, Historical)',
						'jabber:iq:avatar':'Avatar (XEP-0008, Historical)',
						'http://jabberd.jabberstudio.org/ns/component/1.0':'Jabberstudio Component (Jabberd2)',
						'jabber:server:dialback':'Dialback (RFC 3921)',
						'http://jabber.org/protocol/si/profile/file-transfer':'File Transfer (XEP-0096)',
						'presence-invisible':'Presence invisible (Jabberd2)',
						'iq':'Iq (Jabberd2)',
						'message':'Message (Jabberd2)',
						'http://jabber.org/protocol/muc#unique':'Muc Unicue (XEP-0045)',
						'http://jabber.org/protocol/muc#request':'Muc Request (XEP-0045)',
						'http://jabber.org/protocol/muc#rooms':'Muc Rooms (XEP-0045)',
						'http://jabber.org/protocol/muc#traffic':'Muc Traffic (XEP-0045)',
						'http://jabber.org/protocol/nick':'User Nickname (XEP-0172)',
						'http://jabber.org/protocol/nick+notify':'Nick and notify (XEP-0172)',
						'http://jabber.org/protocol/physloc':'Physloc User Geolocation (XEP-0112)',
						'presence':'Presence (Jabberd2)',
						'http://jabber.org/protocol/pubsub':'PubSub (XEP-0060)',
						'http://jabber.org/protocol/rc':'Remote Controllling Clients (XEP-0146)',
						'http://jabber.org/protocol/si':'SI File Transfer (XEP-0096)',
						'http://etherx.jabber.org/streams':'Etherx streams (RFC 3920)',
						'jabber:iq:time':'Iq:time (XEP-0090, Deprecated)',
						'http://jabber.org/protocol/vacation':'Vacalation (XEP-0109)',
						'vcard-temp:x:update':'vCard-Based Avatars (XEP-0153)',
						'http://jabber.org/protocol/stats':'Stats (XEP-0039)',
						'http://jabber.ru/muc-filter':'Muc-filter (Experimental!)',
						'jabber:x:avatar':'Avatar (XEP-0008)',
						'http://jabber.org/protocol/activity+notify':'User activity and notify (XEP-0108)',
						'http://jabber.org/protocol/geoloc+notify':'User Geolocation (XEP-0080)',
						'http://jabber.org/protocol/iqibb':'IqIBB (Unknown)',
						'http://jabber.org/protocol/mood+notify':'User mood and notify (XEP-0107)',
						'http://jabber.org/protocol/tune':'User tune (XEP-0118)',
						'http://jabber.org/protocol/tune+notify':'User tune (XEP-0118)',
						'games:board':'Games board (No XEP)',
						'http://jabber.org/protocol/mute#ancestor':'Multi-User Text Editing Ancestor (XEP-0058)',
						'http://jabber.org/protocol/mute#editor':'Multi-User Text Editing Editor (XEP-0058)',
						'plugins:alarm':'Plugins Alarm (No XEP)',
						'http://www.w3.org/2000/svg':'Whiteboard (XEP-XXXX)',
						'urn:xmpp:attention:0':'Attention (XEP-0224)',
						'urn:xmpp:bob':'Bits of Binary (XEP-0231)',
						'urn:xmpp:jingle:1':'Jingle (XEP-0166)',
						'urn:xmpp:jingle:error:1':'Jingle Error (XEP-0166)',
						'urn:xmpp:jingle:apps:rtp:1':'Jingle RTP Session (XEP-0167)',
						'urn:xmpp:jingle:apps:rtp:errors:1':'Jingle RTP Session Errors (XEP-0167)',
						'urn:xmpp:jingle:apps:rtp:info:1':'Jingle RTP Session Info (XEP-0167)',
						'urn:xmpp:jingle:transports:ice-udp:1':'Jingle ICE-UDP Transport Method (XEP-0176)',
						'urn:xmpp:jingle:transports:raw-udp:1':'Jingle RAW-UDP Transport Method (XEP-0176)',
						'http://jabber.org/protocol/pubsub#errors':'Publish-Subscribe (XEP-0060)',
						'http://jabber.org/protocol/pubsub#event':'Publish-Subscribe (XEP-0060)',
						'http://jabber.org/protocol/pubsub#owner':'Publish-Subscribe (XEP-0060)',
						'jabber:x:conference':'Direct MUC Invitations (XEP-0249)',
						'urn:xmpp:archive':'Message Archiving (XEP-0136)',
						'urn:xmpp:captcha':'CAPTCHA Forms (XEP-0158)',
						'urn:xmpp:errors':'Application-Specific Error Conditions (XEP-0182)',
						'urn:xmpp:langtrans':'Language Translation (XEP-0171)',
						'urn:xmpp:langtrans#items':'Language Translation Items (XEP-0171)',
						'urn:xmpp:media-element':'Data Forms Media Element (XEP-0221)',
						'urn:xmpp:pie':'Portable Import/Export Format for XMPP-IM Servers (XEP-0227)',
						'urn:xmpp:sm:2':'Stream Management (XEP-0198)',
						'urn:xmpp:xbosh':'XMPP Over BOSH (XEP-0206)',
						'http://jabber.org/protocol/sxe':'http://jabber.org/protocol/sxe',
						'http://miranda-im.org/caps/secureim':'http://miranda-im.org/caps/secureim',
						'bugs':'bugs',
						'http://qip.ru/x-status':'http://qip.ru/x-status',
						'http://www.xmpp.org/extensions/xep-0116.html#ns':'Encrypted Session Negotiation (XEP-0116)',
						'urn:xmpp:sec-label:0':'urn:xmpp:sec-label:0',
						'jabber:iq:dtcp':'jabber:iq:dtcp',
						'jabber:iq:filexfer':'jabber:iq:filexfer',
						'jabber:iq:ibb':'jabber:iq:ibb',
						'jabber:iq:inband':'jabber:iq:inband',
						'jabber:iq:jidlink':'jabber:iq:jidlink',
						'urn:xmpp:message-correct:0':'Last Message Correction (XEP-0308)'}

def disco_features_add(i):
	for t in bot_features: i.getTag('query').setTag('feature',attrs={'var':t})
	return i

def disco_ext_info_add(i):
	i.getTag('query').setTag('identity',attrs={'xml:lang':CURRENT_LOCALE,'category':id_category,'type':id_type,'name':id_name})
	i.getTag('query').setTag('x',namespace=xmpp.NS_DATA,attrs={'type':'result'})
	i.getTag('query').getTag('x',namespace=xmpp.NS_DATA).setTag('field',attrs={'var':'FORM_TYPE','type':'hidden'})
	i.getTag('query').getTag('x',namespace=xmpp.NS_DATA).getTag('field',attrs={'var':'FORM_TYPE','type':'hidden'}).setTagData('value',xmpp.NS_SOFTWAREINFO)
	for t in bot_softwareinfo.keys():
		i.getTag('query').getTag('x',namespace=xmpp.NS_DATA).setTag('field',attrs={'var':t})
		i.getTag('query').getTag('x',namespace=xmpp.NS_DATA).getTag('field',attrs={'var':t}).setTagData('value',bot_softwareinfo[t])
	return i

def disco_iq_get(iq,id,room,acclvl,query,towh,al):
	if iq.getTag(name='query', namespace=xmpp.NS_DISCO_INFO):
		node=get_tag_item(unicode(query),'query','node')
		if node.split('#')[0] in ['', disco_config_node, xmpp.NS_COMMANDS] or node in [xmpp.NS_MUC_ROOMS, '%s#%s' % (capsNode,capsHash)]:
			pprint('*** iq:disco_info from %s node "%s"' % (unicode(room),node),'magenta')
			i=xmpp.Iq(to=room, typ='result')
			i.setAttr(key='id', val=id)
			if node == '': i.setQueryNS(namespace=xmpp.NS_DISCO_INFO)
			else: i.setTag('query',namespace=xmpp.NS_DISCO_INFO,attrs={'node':node})
			if node == '' or node == '%s#%s' % (capsNode,capsHash):
				i = disco_features_add(i)
				sender(disco_ext_info_add(i))
				raise xmpp.NodeProcessed
			elif node == xmpp.NS_MUC_ROOMS:
				#i.getTag('query').setTag('feature',attrs={'var':xmpp.NS_MUC_ROOMS})
				return i
			elif node.split('#')[0] == disco_config_node or node == xmpp.NS_COMMANDS:
				if node != xmpp.NS_COMMANDS:
					i.getTag('query').setTag('feature',attrs={'var':xmpp.NS_COMMANDS})
					#i.getTag('query').setTag('feature',attrs={'var':disco_config_node})
					#i.getTag('query').setTag('feature',attrs={'var':xmpp.NS_DATA})
				try: tn = '#' + node.split('#')[1]
				except: tn = ''
				if tn:
					if tn.split('-',1)[0] == '#owner': settz = owner_groups
					elif tn.split('-',1)[0] == '#room': settz = config_groups
					else: settz = None
					if settz:
						for tmp in settz:
							if tn == tmp[1]:
								i.getTag('query').setTag('identity',attrs={'category':'automation','type':'command-node','name':tmp[0]})
								break
				return i

	elif iq.getTag(name='query', namespace=xmpp.NS_DISCO_ITEMS):
		node=get_tag_item(unicode(query),'query','node')
		pprint('*** iq:disco_items from %s node "%s"' % (unicode(room),node),'magenta')
		if node == xmpp.NS_MUC_ROOMS and GT('iq_show_rooms_disco'):
				i=xmpp.Iq(to=room, typ='result')
				i.setAttr(key='id', val=id)
				i.setTag('query',namespace=xmpp.NS_DISCO_ITEMS,attrs={'node':node})
				if al == 9: cnf = cur_execute_fetchall("select room from conference;")
				else: cnf = cur_execute_fetchall("select room from conference where split_part(room,'/',1) not in (select room from hiden_rooms as hrr);")
				trooms = [t[0] for t in cnf]
				trooms.sort()
				trooms = [xmpp.Node('item',attrs={'jid':t}) for t in trooms]
				i.getTag('query',namespace=xmpp.NS_DISCO_ITEMS).setPayload(trooms)
				return i
		elif node.split('#')[0] in [disco_config_node, xmpp.NS_COMMANDS] and acclvl:
			try: tn = '#' + node.split('#')[1]
			except: tn = ''
			i=xmpp.Iq(to=room, typ='result')
			i.setAttr(key='id', val=id)
			if node == '': i.setQueryNS(namespace=xmpp.NS_DISCO_ITEMS)
			else: i.setTag('query',namespace=xmpp.NS_DISCO_ITEMS,attrs={'node':node})
			if node == '' or node == xmpp.NS_COMMANDS:
				if towh == selfjid: settings_set = owner_groups
				else: settings_set = config_groups
				for tmp in settings_set: i.getTag('query').setTag('item',attrs={'node':disco_config_node+tmp[1], 'name':L(tmp[0],room),'jid':towh})
			return i
		elif node == '' and al > 3:
			i=xmpp.Iq(to=room, typ='result')
			i.setAttr(key='id', val=id)
			i.setQueryNS(namespace=xmpp.NS_DISCO_ITEMS)
			if acclvl: i.getTag('query').setTag('item',attrs={'node':xmpp.NS_COMMANDS, 'name':L('AD-Hoc commands'),'jid':towh})
			i.getTag('query').setTag('item',attrs={'node':xmpp.NS_MUC_ROOMS, 'name':L('Current bot rooms'),'jid':towh})
			return i
	return None

def disco_iq_set(iq,id,room,acclvl,query,towh,al):
	if iq.getTag(name='command', namespace=xmpp.NS_COMMANDS) and acclvl:
		node=get_tag_item(unicode(iq),'command','node')
		if get_tag_item(unicode(iq),'command','action') == 'execute' and (node.split('#')[0] in ['', disco_config_node, xmpp.NS_COMMANDS] or node == xmpp.NS_MUC_ROOMS):
			pprint('*** iq:ad-hoc commands from %s node "%s"' % (unicode(room),node),'magenta')
			i=xmpp.Iq(to=room, typ='result')
			i.setAttr(key='id', val=id)
			if node == '': i.setQueryNS(namespace=xmpp.NS_DISCO_INFO)
			else: i.setTag('query',namespace=xmpp.NS_DISCO_ITEMS,attrs={'node':node})
			if node == '':
				i = disco_features_add(i)
				sender(disco_ext_info_add(i))
				raise xmpp.NodeProcessed
			elif node == xmpp.NS_MUC_ROOMS and GT('iq_show_rooms_disco'):
				if al == 9: cnf = cur_execute_fetchall("select room from conference;")
				else: cnf = cur_execute_fetchall("select room from conference where split_part(room,'/',1) not in (select room from hiden_rooms as hrr);")
				trooms = [t[0] for t in cnf]
				trooms.sort()
				trooms = [xmpp.Node('item',attrs={'jid':t}) for t in trooms]
				i.getTag('query',namespace=xmpp.NS_DISCO_ITEMS).setPayload(trooms)
				return i
			elif node.split('#')[0] == disco_config_node or node == xmpp.NS_COMMANDS:
				if node != xmpp.NS_COMMANDS:
					i.getTag('query').setTag('feature',attrs={'var':xmpp.NS_COMMANDS})
					#i.getTag('query').setTag('feature',attrs={'var':xmpp.NS_DATA})
					#i.getTag('query').setTag('feature',attrs={'var':disco_config_node})
				try: tn = '#' + node.split('#')[1]
				except: tn = ''
				try: tmpn = tn.split('-',1)[1]
				except: tmpn = ''
				if tmpn:
					action=get_tag_item(unicode(iq),'command','action')
					i=xmpp.Iq(to=room, typ='result')
					i.setAttr(key='id', val=id)
					if action == 'cancel': i.setTag('command',namespace=xmpp.NS_COMMANDS,attrs={'status':'canceled', 'node':disco_config_node+tn,'sessionid':id})
					elif towh == selfjid:
						if get_tag_item(unicode(iq),'x','type') == 'submit':
							varz = iq.getTag('command').getTag('x')
							sucess_label,unsucess = True,[]
							for t in owner_prefs.keys():
								try:
									tp = owner_prefs[t][1]
									tm = varz.getTag('field',attrs={'var':t}).getTags('value')
									tm = '\n'.join([tm2.getData() for tm2 in tm])
									old_tm = GT(t)
									try:
										if   tp[0] == 'b': tm = [False,True][int(tm)]
										elif tp[0] == 'f': tm = float(tm)
										elif tp[0] == 'i': tm = int(tm)
										elif tp[0] == 't': tm = tm[:int(tp.replace('e','')[1:])]
										elif tp[0] == 'm': tm = tm[:int(tp.replace('e','')[1:])]
										elif tp[0] == 'l' and len(json.loads(tm)) == int(tp.replace('e','')[1:]): tm = json.loads(tm)
										elif tp[0] == 'd' and tm not in owner_prefs[t][3]: tm = owner_prefs[t][2]
									except:
										tm,sucess_label = GT(t),False
										unsucess.append(L(owner_prefs[t][0],room))
									PT(t,tm)
									if tp[-1] == 'e' and old_tm != tm: eval(owner_prefs[t][-1])
								except: pass
							sucess_answer = [L('Settings unsuccesfully accepted:\n%s',room) % '\n'.join(unsucess),L('Settings succesfully accepted',room)][sucess_label]
							i.setTag('command',namespace=xmpp.NS_COMMANDS,attrs={'status':'completed', 'node':disco_config_node+tn,'sessionid':id})
							i.getTag('command').setTag('note',attrs={'type':'info'})
							i.getTag('command').setTagData('note',sucess_answer)
							i.getTag('command').setTag('x',namespace=xmpp.NS_DATA)
							i.getTag('command').getTag('x').setTagData('title',L('Settings',room))
							i.getTag('command').getTag('x').setTagData('instrustion',sucess_answer)
							pprint('*** bot reconfigure by %s' % unicode(room),'purple')
						else:
							i.setTag('command',namespace=xmpp.NS_COMMANDS,attrs={'status':'executing', 'node':disco_config_node+tn,'sessionid':id})
							i.getTag('command').setTag('x',namespace=xmpp.NS_DATA,attrs={'type':'form'})
							#i.getTag('command').getTag('x').setTag('item',attrs={'node':disco_config_node+tn, 'name':'Configuration','jid':selfjid})
							#i.getTag('command').getTag('x').setTagData('instructions',L('For configure required x:data-compatible client',room))
							tkeys = []
							for tmp in owner_groups: tkeys.append(tmp[1])
							if tn in tkeys:
								for tmp in owner_groups:
									if tn == tmp[1]:
										c_prefs,c_name = tmp[2],tmp[0]
										break
								i.getTag('command').getTag('x').setTagData('title',L(c_name,room))
								cnf_prefs = {}
								for tmp in c_prefs: cnf_prefs[tmp] = owner_prefs[tmp]
								tmp = cnf_prefs.keys()
								tt = []
								for t in tmp: tt.append((L(owner_prefs[t][0],room),t))
								tt.sort()
								tmp = []
								for t in tt: tmp.append(t[1])
								for t in tmp:
									itm = owner_prefs[t]
									itm_label = L(itm[0],room).replace('%s','').replace(':','').strip()
									if itm[1][0] == 'b':
										dc = GT(t) in [True,1,'1','on']
										i.getTag('command').getTag('x').setTag('field',attrs={'type':'boolean','label':itm_label,'var':t})\
										.setTagData('value',[0,1][dc])
									elif itm[1][0] in ['t','i','f','l']:
										i.getTag('command').getTag('x').setTag('field',attrs={'type':'text-single','label':itm_label,'var':t})\
										.setTagData('value',unicode(GT(t)))
									elif itm[1][0] == 'm':
										tprm = [xmpp.Node('value',payload=prm) for prm in unicode(GT(t)).split('\n')]
										i.getTag('command').getTag('x').setTag('field',attrs={'type':'text-multi','label':itm_label,'var':t})\
										.setPayload(tprm)
									else:
										i.getTag('command').getTag('x').setTag('field',\
										attrs={'type':'list-single','label':itm_label,'var':t})\
										.setTagData('value',GT(t))
										for t2 in itm[3]:
											i.getTag('command').getTag('x').getTag('field',\
											attrs={'type':'list-single','label':itm_label,'var':t})\
											.setTag('option',attrs={'label':L(t2,room)})\
											.setTagData('value',t2)
					else:
						if get_tag_item(unicode(iq),'x','type') == 'submit':
							varz = iq.getTag('command').getTag('x')
							for t in config_prefs.keys():
								try:
									tmtype = varz.getTagAttr('field','type')
									tm = varz.getTag('field',attrs={'var':t}).getTags('value')
									tm = '\n'.join([tm2.getData() for tm2 in tm])
									if tmtype == 'boolean' and tm in ['0','1']: tm = [False,True][int(tm)]
									elif config_prefs[t][2] != None:
										if config_prefs[t][2] == [True,False] and tm in ['0','1']: tm = [False,True][int(tm)]
										elif tm in config_prefs[t][2]: pass
										else: tm = config_prefs[t][3]
									put_config(getRoom(room),t,tm)
								except: pass
							sucess_answer = L('Settings succesfully accepted',room)
							i.setTag('command',namespace=xmpp.NS_COMMANDS,attrs={'status':'completed', 'node':disco_config_node+tn,'sessionid':id})
							i.getTag('command').setTag('note',attrs={'type':'info'})
							i.getTag('command').setTagData('note',sucess_answer)
							i.getTag('command').setTag('x',namespace=xmpp.NS_DATA)
							i.getTag('command').getTag('x').setTagData('title',L('Settings',room))
							i.getTag('command').getTag('x').setTagData('instrustion',sucess_answer)
							pprint('*** reconfigure by %s' % unicode(room),'purple')
						else:
							i.setTag('command',namespace=xmpp.NS_COMMANDS,attrs={'status':'executing', 'node':disco_config_node+tn,'sessionid':id})
							i.getTag('command').setTag('x',namespace=xmpp.NS_DATA,attrs={'type':'form'})
							#i.getTag('command').getTag('x').setTag('item',attrs={'node':disco_config_node+tn, 'name':'Configuration','jid':selfjid})
							#i.getTag('command').getTag('x').setTagData('instructions',L('For configure required x:data-compatible client',room))
							tkeys = []
							for tmp in config_groups: tkeys.append(tmp[1])
							if tn in tkeys:
								for tmp in config_groups:
									if tn == tmp[1]:
										c_prefs,c_name = tmp[2],tmp[0]
										break
								i.getTag('command').getTag('x').setTagData('title',L(c_name,room))
								cnf_prefs = {}
								for tmp in c_prefs: cnf_prefs[tmp] = config_prefs[tmp]
								tmp = cnf_prefs.keys()
								tmp.sort()
								for t in tmp:
									itm = config_prefs[t]
									itm_label = L(itm[0],room).replace('%s','').replace(':','').strip()
									itm_desc = L(itm[1],room).strip()
									if itm[2] == [True,False]:
										dc = get_config(getRoom(room),t) in [True,1,'1','on']
										i.getTag('command').getTag('x').setTag('field',attrs={'type':'boolean','label':itm_label,'var':t})\
										.setTagData('value',[0,1][dc])
									elif itm[2] == None:
										if '\n' in itm[3]:
											tprm = [xmpp.Node('value',payload=prm) for prm in get_config(getRoom(room),t).split('\n')]
											i.getTag('command').getTag('x').setTag('field',attrs={'type':'text-multi','label':itm_label,'var':t})\
											.setPayload(tprm)
										else:
											i.getTag('command').getTag('x').setTag('field',attrs={'type':'text-single','label':itm_label,'var':t})\
											.setTagData('value',get_config(getRoom(room),t))
									else:
										i.getTag('command').getTag('x').setTag('field',\
										attrs={'type':'list-single','label':itm_label,'var':t})\
										.setTagData('value',get_config(getRoom(room),t))
										for t2 in itm[2]:
											i.getTag('command').getTag('x').getTag('field',\
											attrs={'type':'list-single','label':itm_label,'var':t})\
											.setTag('option',attrs={'label':onoff(t2,room)})\
											.setTagData('value',t2)
									i.getTag('command').getTag('x').getTag('field',attrs={'label':itm_label,'var':t})\
									.setTagData('desc',itm_desc)

							else: i.getTag('command').getTag('x').setTagData('title',L('Unknown configuration request!',room))
					return i
				else:
					if tn:
						if tn.split('-',1)[0] == '#owner': settz = owner_groups
						elif tn.split('-',1)[0] == '#room': settz = config_groups
						else: settz = None
						if settz:
							for tmp in settz:
								if tn == tmp[1]:
									i.getTag('query').setTag('identity',attrs={'category':'automation','type':'command-node','name':tmp[0]})
									break
					return i
		else:
			pprint('*** iq:disco_set from %s node "%s"' % (unicode(room),node),'magenta')
			try: tn = '#' + node.split('#')[1]
			except: tn = ''
			if node.split('#')[0] == disco_config_node or node == xmpp.NS_COMMANDS:
				action=get_tag_item(unicode(iq),'command','action')
				i=xmpp.Iq(to=room, typ='result')
				i.setAttr(key='id', val=id)
				if action == 'cancel': i.setTag('command',namespace=xmpp.NS_COMMANDS,attrs={'status':'canceled', 'node':disco_config_node+tn,'sessionid':id})
				elif towh == selfjid:
					if get_tag_item(unicode(iq),'x','type') == 'submit':
						varz = iq.getTag('command').getTag('x')
						sucess_label,unsucess = True,[]
						for t in owner_prefs.keys():
							try:
								tp = owner_prefs[t][1]
								tm = varz.getTag('field',attrs={'var':t}).getTags('value')
								tm = '\n'.join([tm2.getData() for tm2 in tm])
								old_tm = GT(t)
								try:
									if   tp[0] == 'b': tm = [False,True][int(tm)]
									elif tp[0] == 'f': tm = float(tm)
									elif tp[0] == 'i': tm = int(tm)
									elif tp[0] == 't': tm = tm[:int(tp.replace('e','')[1:])]
									elif tp[0] == 'm': tm = tm[:int(tp.replace('e','')[1:])]
									elif tp[0] == 'l' and len(json.loads(tm)) == int(tp.replace('e','')[1:]): tm = json.loads(tm)
									elif tp[0] == 'd' and tm not in owner_prefs[t][3]: tm = owner_prefs[t][2]
								except:
									tm,sucess_label = GT(t),False
									unsucess.append(L(owner_prefs[t][0],room))
								PT(t,tm)
								if tp[-1] == 'e' and old_tm != tm: eval(owner_prefs[t][-1])
							except: pass
						sucess_answer = [L('Settings unsuccesfully accepted:\n%s',room) % '\n'.join(unsucess),L('Settings succesfully accepted',room)][sucess_label]
						i.setTag('command',namespace=xmpp.NS_COMMANDS,attrs={'status':'completed', 'node':disco_config_node+tn,'sessionid':id})
						i.getTag('command').setTag('note',attrs={'type':'info'})
						i.getTag('command').setTagData('note',sucess_answer)
						i.getTag('command').setTag('x',namespace=xmpp.NS_DATA)
						i.getTag('command').getTag('x').setTagData('title',L('Settings',room))
						i.getTag('command').getTag('x').setTagData('instrustion',sucess_answer)
						pprint('*** bot reconfigure by %s' % unicode(room),'purple')
					else:
						i.setTag('command',namespace=xmpp.NS_COMMANDS,attrs={'status':'executing', 'node':disco_config_node+tn,'sessionid':id})
						i.getTag('command').setTag('x',namespace=xmpp.NS_DATA,attrs={'type':'form'})
						#i.getTag('command').getTag('x').setTag('item',attrs={'node':disco_config_node+tn, 'name':'Configuration','jid':selfjid})
						#i.getTag('command').getTag('x').setTagData('instructions',L('For configure required x:data-compatible client',room))
						tkeys = []
						for tmp in owner_groups: tkeys.append(tmp[1])
						if tn in tkeys:
							for tmp in owner_groups:
								if tn == tmp[1]:
									c_prefs,c_name = tmp[2],tmp[0]
									break
							i.getTag('command').getTag('x').setTagData('title',L(c_name,room))
							cnf_prefs = {}
							for tmp in c_prefs: cnf_prefs[tmp] = owner_prefs[tmp]
							tmp = cnf_prefs.keys()
							tt = []
							for t in tmp: tt.append((L(owner_prefs[t][0],room),t))
							tt.sort()
							tmp = []
							for t in tt: tmp.append(t[1])
							for t in tmp:
								itm = owner_prefs[t]
								itm_label = L(itm[0],room).replace('%s','').replace(':','').strip()
								if itm[1] == 'b':
									dc = GT(t) in [True,1,'1','on']
									i.getTag('command').getTag('x').setTag('field',attrs={'type':'boolean','label':itm_label,'var':t})\
									.setTagData('value',[0,1][dc])
								elif itm[1][0] in ['t','i','f','l']:
									i.getTag('command').getTag('x').setTag('field',attrs={'type':'text-single','label':itm_label,'var':t})\
									.setTagData('value',unicode(GT(t)))
								elif itm[1][0] == 'm':
									tprm = [xmpp.Node('value',payload=prm) for prm in unicode(GT(t)).split('\n')]
									i.getTag('command').getTag('x').setTag('field',attrs={'type':'text-multi','label':itm_label,'var':t})\
									.setPayload(tprm)
								else:
									i.getTag('command').getTag('x').setTag('field',\
									attrs={'type':'list-single','label':itm_label,'var':t})\
									.setTagData('value',GT(t))
									for t2 in itm[3]:
										i.getTag('command').getTag('x').getTag('field',\
										attrs={'type':'list-single','label':itm_label,'var':t})\
										.setTag('option',attrs={'label':L(t2,room)})\
										.setTagData('value',t2)
				else:
					if get_tag_item(unicode(iq),'x','type') == 'submit':
						varz = iq.getTag('command').getTag('x')
						for t in config_prefs.keys():
							try:
								tmtype = varz.getTagAttr('field','type')
								tm = varz.getTag('field',attrs={'var':t}).getTags('value')
								tm = '\n'.join([tm2.getData() for tm2 in tm])
								if tmtype == 'boolean' and tm in ['0','1']: tm = [False,True][int(tm)]
								elif config_prefs[t][2] != None:
									if config_prefs[t][2] == [True,False] and tm in ['0','1']: tm = [False,True][int(tm)]
									elif tm in config_prefs[t][2]: pass
									else: tm = config_prefs[t][3]
								put_config(getRoom(room),t,tm)
							except: pass
						sucess_answer = L('Settings succesfully accepted',room)
						i.setTag('command',namespace=xmpp.NS_COMMANDS,attrs={'status':'completed', 'node':disco_config_node+tn,'sessionid':id})
						i.getTag('command').setTag('note',attrs={'type':'info'})
						i.getTag('command').setTagData('note',sucess_answer)
						i.getTag('command').setTag('x',namespace=xmpp.NS_DATA)
						i.getTag('command').getTag('x').setTagData('title',L('Settings',room))
						i.getTag('command').getTag('x').setTagData('instrustion',sucess_answer)

						pprint('*** reconfigure by %s' % unicode(room),'purple')
					else:
						i.setTag('command',namespace=xmpp.NS_COMMANDS,attrs={'status':'executing', 'node':disco_config_node+tn,'sessionid':id})
						i.getTag('command').setTag('x',namespace=xmpp.NS_DATA,attrs={'type':'form'})
						#i.getTag('command').getTag('x').setTag('item',attrs={'node':disco_config_node+tn, 'name':'Configuration','jid':selfjid})
						#i.getTag('command').getTag('x').setTagData('instructions',L('For configure required x:data-compatible client',room))
						tkeys = []
						for tmp in config_groups: tkeys.append(tmp[1])
						if tn in tkeys:
							for tmp in config_groups:
								if tn == tmp[1]:
									c_prefs,c_name = tmp[2],tmp[0]
									break
							i.getTag('command').getTag('x').setTagData('title',L(c_name,room))
							cnf_prefs = {}
							for tmp in c_prefs: cnf_prefs[tmp] = config_prefs[tmp]
							tmp = cnf_prefs.keys()
							tmp.sort()
							for t in tmp:
								itm = config_prefs[t]
								itm_label = L(itm[0],room).replace('%s','').replace(':','').strip()
								itm_desc = L(itm[1],room).strip()
								if itm[2] == [True,False]:
									dc = get_config(getRoom(room),t) in [True,1,'1','on']
									i.getTag('command').getTag('x').setTag('field',attrs={'type':'boolean','label':itm_label,'var':t})\
									.setTagData('value',[0,1][dc])
								elif itm[2] == None:
									if '\n' in itm[3]:
										tprm = [xmpp.Node('value',payload=prm) for prm in get_config(getRoom(room),t).split('\n')]
										i.getTag('command').getTag('x').setTag('field',attrs={'type':'text-multi','label':itm_label,'var':t})\
										.setPayload(tprm)
									else:
										i.getTag('command').getTag('x').setTag('field',attrs={'type':'text-single','label':itm_label,'var':t})\
										.setTagData('value',get_config(getRoom(room),t))
								else:
									i.getTag('command').getTag('x').setTag('field',\
									attrs={'type':'list-single','label':itm_label,'var':t})\
									.setTagData('value',get_config(getRoom(room),t))
									for t2 in itm[2]:
										i.getTag('command').getTag('x').getTag('field',\
										attrs={'type':'list-single','label':itm_label,'var':t})\
										.setTag('option',attrs={'label':onoff(t2,room)})\
										.setTagData('value',t2)
								i.getTag('command').getTag('x').getTag('field',attrs={'label':itm_label,'var':t})\
								.setTagData('desc',itm_desc)
						else: i.getTag('command').getTag('x').setTagData('title',L('Unknown configuration request!',room))
				return i
	return None

def disco_exclude_update():
	global disco_excl
	excl = GT('disco_exclude').replace('\r','').replace('\t','').split('\n')
	disco_excl = []
	for c in excl:
		if '#' not in c and len(c): disco_excl.append(c)

def disco_validate(item):
	for c in disco_excl:
		if re.findall(c,' %s ' % item,re.S|re.I|re.U): return None
	return item

def smart_sort(item):
	itm1,itm2,cnt = [],[],0
	for t in item:
		itm1.append([t.lower(),cnt])
		cnt += 1
	itm1.sort()
	for t in itm1: itm2.append(item[t[1]])
	return itm2

def features(type, jid, nick, text):
	global iq_answer,iq_request
	text = text.strip()
	if text == '': where,what = '%s/%s' % (getRoom(jid),nick),''
	else:
		text = text.split('\n')
		where = text[0]
		try: what = text[1]
		except: what = ''
		for mega1 in megabase:
			if mega1[0] == jid and mega1[1] == text[0]:
				where = '%s/%s' % (getRoom(jid),text[0])
				break
	iqid = get_id()
	i = xmpp.Node('iq', {'id': iqid, 'type': 'get', 'to':where}, payload = [xmpp.Node('query', {'xmlns': xmpp.NS_DISCO_INFO},[])])
	iq_request[iqid]=(time.time(),features_async,[type, jid, nick, what, where],xmpp.NS_DISCO_INFO)
	sender(i)

def features_async(type, jid, nick, what, where, is_answ):
	isa = is_answ[1]	
	if len(isa) >= 2 and isa[1] == 'error': msg = L('Error! %s','%s/%s'%(jid,nick)) % L(isa[0].capitalize().replace('-',' '),'%s/%s'%(jid,nick))
	else:
		isa, ftr, client_features = isa[1], [], []
		for f in [t.getAttr('var') for t in isa.getTag('query',namespace=xmpp.NS_DISCO_INFO).getTags('feature')]:
			client_features.append(f)
			if disco_features_list.has_key(f): ft = '- %s' % disco_features_list[f]
			else: ft = L('- Unknown feature: %s','%s/%s'%(jid,nick)) % f
			if (what and (what.lower() in ft.lower() or what.lower() in f.lower())) or not what: ftr.append(ft)

		ftrs,erc,q_features = {},0,['os_version','os','software_version','software']
		client_softwareinfo = {}
		for t in q_features:
			try:
				res = isa.getTag('query').getTag('x',namespace=xmpp.NS_DATA).getTag('field',attrs={'var':t}).getTagData('value')
				client_softwareinfo[t] = res
			except:
				res = 'N/A'
				erc += 1
			ftrs[t] = res

		if erc != len(q_features):
			f = L('Software: %s | Version: %s\nOS: %s | Version: %s','%s/%s'%(jid,nick)) % (ftrs['software'],ftrs['software_version'],ftrs['os'],ftrs['os_version'])
			if (what and what.lower() in f.lower()) or not what: ftr.append(f)
		id_category,id_type,id_name,id_lang = '','','',''
		try:
			ids_t = isa.getTag('query').getTags('identity')
			idk = {'type':L('Type: %s','%s/%s'%(jid,nick)), 'name':L('Name: %s','%s/%s'%(jid,nick)), 'category':L('Category: %s','%s/%s'%(jid,nick)), 'xml:lang':L('Language: %s','%s/%s'%(jid,nick))}
			for tg in ids_t:
				ids = tg.getAttrs()
				idf = []
				for t in idk.keys():
					if ids.has_key(t):
						idf.append(idk[t] % ids[t])
						if t == 'type': id_type = ids[t]
						elif t == 'name': id_name = ids[t]
						elif t == 'category': id_category = ids[t]
						elif t == 'xml:lang': id_lang = ids[t]
				if idf:
					f = ' | '.join(idf)
					if (what and what.lower() in f.lower()) or not what: ftr.append(f)
		except: pass

		if ftr:
			f = []
			for tmp in ftr:
				if tmp not in f: f.append(tmp)
			f.sort()
			msg = L('Features list:\n%s','%s/%s'%(jid,nick)) % '\n'.join(f)
			_hash = '%s<' % '/'.join([t.replace('/','//') for t in [id_category,id_type,id_lang,id_name]])
			client_features.sort()
			_hash += ''.join(['%s<' % t for t in client_features])
			if client_softwareinfo:
				_hash += '%s<' % xmpp.NS_SOFTWAREINFO
				tmp = ['%s<%s' % (t,client_softwareinfo[t]) for t in client_softwareinfo.keys()]
				tmp.sort()
				_hash += ''.join(['%s<' % t for t in tmp])
			_hash = _hash.encode('utf-8')
			_hash_sha1 = 'SHA1: %s' % hashlib.sha1(_hash).digest().encode('base64').replace('\n','')
			_hash_md5 = 'MD5: %s' % hashlib.md5(_hash).digest().encode('base64').replace('\n','')
			_hashes = '%s | %s' % (_hash_sha1,_hash_md5)
			if (what and what.lower() in _hashes.lower()) or not what: msg = '%s\n%s' % (msg, _hashes)
		else: msg = L('Unable to get features list','%s/%s'%(jid,nick))
	send_msg(type, jid, nick, msg)

def disco(type, jid, nick, text): disco_r(type, jid, nick, text, True)
def disco_raw(type, jid, nick, text): disco_r(type, jid, nick, text, False)

def disco_r(type, jid, nick, text, raw_type):
	global iq_answer,iq_request
	text = text.strip()
	if text == '':
		send_msg(type, jid, nick, L('What?','%s/%s'%(jid,nick)))
		return
	where = text.lower().split('\n',1)[0].split(' ',1)[0]
	try: what = text.lower().split('\n',1)[0].split(' ',1)[1]
	except: what = ''
	try: hm = int(text.lower().split('\n',1)[1])
	except: hm = GT('disco_max_limit')
	iqid = get_id()
	i = xmpp.Node('iq', {'id': iqid, 'type': 'get', 'to':where}, payload = [xmpp.Node('query', {'xmlns': xmpp.NS_DISCO_INFO},[])])
	iq_request[iqid]=(time.time(),disco_features_async,[type, jid, nick, what, where, hm, raw_type],xmpp.NS_DISCO_INFO)
	sender(i)

def disco_features_async(type, jid, nick, what, where, hm, raw_type, is_answ):
	isa = is_answ[1]
	if len(isa) >= 2 and isa[1] == 'error':
		msg = L('Error! %s','%s/%s'%(jid,nick)) % L(isa[0].capitalize().replace('-',' '),'%s/%s'%(jid,nick))
		send_msg(type, jid, nick, msg)
		return
	else:
		disco_type = xmpp.NS_MUC in [t.getAttr('var') for t in isa[1].getTag('query',namespace=xmpp.NS_DISCO_INFO).getTags('feature')]
		iqid = get_id()
		i = xmpp.Node('iq', {'id': iqid, 'type': 'get', 'to':where}, payload = [xmpp.Node('query', {'xmlns': xmpp.NS_DISCO_ITEMS},[])])
		iq_request[iqid]=(time.time(),disco_async,[type, jid, nick, what, where, hm, disco_type, raw_type, isa[1]],xmpp.NS_DISCO_ITEMS)
		sender(i)

def disco_async(type, jid, nick, what, where, hm, disco_type, raw_type, isa_prev, is_answ):
	if len(is_answ[1]) >= 2 and is_answ[1][1] == 'error': msg = L('Error! %s','%s/%s'%(jid,nick)) % L(is_answ[1][0].capitalize().replace('-',' '),'%s/%s'%(jid,nick))
	else:
		if disco_type and '@' not in where:
			cm = []
			for ii in [[t.getAttr('name'),t.getAttr('jid')] for t in is_answ[1][1].getTag('query',namespace=xmpp.NS_DISCO_ITEMS).getTags('item')]:
				dname,djid = ii
				if not dname: dname = ''
				elif '(' in dname and ')' in dname:
					try: dsize = int(dname.split('(')[-1].split(')')[0])
					except: dsize = -1
					dname = '('.join(dname.split('(')[:-1])
				else: dsize = -1
				if dname == djid: djid = ''
				if not what or what in dname.lower() or what in djid.lower():
					if raw_type and disco_validate(dname) and disco_validate(djid): cm.append(('%04d' % dsize, dname, djid))
					elif not raw_type: cm.append(('%04d' % dsize, dname, djid))
			if len(cm):
				cm.sort(reverse=True)
				msg,cnt = L('Total: %s','%s/%s'%(jid,nick)) % len(cm),1
				for i in cm[:hm]:
					vl = [int(i[0]),'n/a'][int(i[0]) == -1]
					if len(i[2]): msg += '\n%s. %s [%s] . %s' % (cnt,i[1],i[2],vl)
					else: msg += '\n%s. %s . %s' % (cnt,i[1],vl)
					cnt += 1
				while '  ' in msg: msg = msg.replace('  ',' ')
			elif len(what): msg = L('\"%s\" not found','%s/%s'%(jid,nick)) % what
			else: msg = L('Not found.','%s/%s'%(jid,nick))
		elif disco_type and '@' in where:
			cm = []
			for ii in [t.getAttr('name') for t in is_answ[1][1].getTag('query',namespace=xmpp.NS_DISCO_ITEMS).getTags('item')]:
				if ii and (not what or what in ii.lower()): cm.append(ii)
			cm = smart_sort(cm)
			if len(cm):
				d_name = reduce_spaces_all(isa_prev.getTag('query',namespace=xmpp.NS_DISCO_INFO).getTagAttr('identity','name'))
				d_deskr = reduce_spaces_all(isa_prev.getTag('query',namespace=xmpp.NS_DISCO_INFO).getTag('x',namespace=xmpp.NS_DATA).getTag('field',attrs={'var':'muc#roominfo_description'}).getTagData('value'))
				d_occup = isa_prev.getTag('query',namespace=xmpp.NS_DISCO_INFO).getTag('x',namespace=xmpp.NS_DATA).getTag('field',attrs={'var':'muc#roominfo_occupants'}).getTagData('value')
				if d_name == d_deskr or not d_deskr: msg = '%s\n%s' % (d_name,L('Total: %s%s','%s/%s'%(jid,nick)) % (d_occup,' - %s' % ', '.join(cm)))
				else: msg = '%s [%s]\n%s' % (d_name,d_deskr,L('Total: %s%s','%s/%s'%(jid,nick)) % (d_occup,' - %s' % ', '.join(cm)))
			elif len(what): msg = L('\"%s\" not found','%s/%s'%(jid,nick)) % what
			else: msg = L('Not found.','%s/%s'%(jid,nick))
		else:
			cm = [t.getAttrs() for t in is_answ[1][1].getTag('query',namespace=xmpp.NS_DISCO_ITEMS).getTags('item')]
			if len(cm):
				cm.sort()
				cnt = 1
				msg = L('Total: %s','%s/%s'%(jid,nick)) % len(cm)
				for i in cm[:hm]:
					msg += '\n%s. ' % cnt
					if i.has_key('name'):
						msg += '%s ' % i['name']
						if i.has_key('node'): msg += '[%s] ' % i['node']
					msg += '%s' % i['jid']
					cnt += 1
			else: msg = L('Not found.','%s/%s'%(jid,nick))
	msg = rss_replace(msg)
	send_msg(type, jid, nick, msg)

def whereis(type, jid, nick, text):
	global iq_request,whereis_lock
	if whereis_lock: send_msg(type, jid, nick, L('This command in use somewhere else. Please try later.','%s/%s'%(jid,nick)))
	else:
		if len(text):
			text = text.split('\n')
			who = text[0]
		else: who = nick
		if len(text)<2: where = getServer(jid)
		else:
			if 'conference' in text[1]: where = text[1]
			else: where = 'conference.'+text[1]
		iqid = get_id()
		i = xmpp.Node('iq', {'id': iqid, 'type': 'get', 'to':where}, payload = [xmpp.Node('query', {'xmlns': xmpp.NS_DISCO_ITEMS},[])])
		iq_request[iqid]=(time.time(),whereis_async,[type, jid, nick, who, where],xmpp.NS_DISCO_ITEMS)
		sender(i)

def whereis_async(type, jid, nick, who, where, is_answ):
	global iq_request, whereis_answers, whereis_lock
	isan = unicode(is_answ[1][0])
	isa = isan.split('<item ')
	djids = []
	for ii in isa[1:]:
		dname = get_subtag(ii,'name').split('(')[-1][:-1]
		if dname.isdigit() and dname != '0': djids.append(get_subtag(ii,'jid'))
	send_msg(type, jid, nick, L('Please wait. Result you will be receive in private message approximately %s %s','%s/%s'%(jid,nick)) % (int(len(djids)*(time_nolimit+0.05)), L('sec.','%s/%s'%(jid,nick))))
	curr_id = 'whereis_%s' % get_id()
	whereis_lock = True
	wtd = GT('whereis_time_dec')
	whereis_id = get_id()
	whereis_answers[whereis_id] = []
	for ii in djids:
		iqid = get_id()
		i = xmpp.Node('iq', {'id': iqid, 'type': 'get', 'to':ii}, payload = [xmpp.Node('query', {'xmlns': xmpp.NS_DISCO_ITEMS},[])])
		iq_request[iqid]=(time.time(),whereis_collect_async,[whereis_id,who],xmpp.NS_DISCO_ITEMS)
		sender(i)
		if game_over: return
	while len(whereis_answers[whereis_id]) != len(djids) and not game_over: time.sleep(wtd)
	if game_over: return
	result = []
	for t in whereis_answers[whereis_id]:
		if t: result += t
	whereis_answers.pop(whereis_id)
	result.sort()
	if result:
		msgg = L('matches with nick \"%s\": %s','%s/%s'%(jid,nick)) % (who, len(result))
		for i in result: msgg += '\n%s\t%s' % (esc_min(i[0]),esc_min(i[1]))
	else: msgg = L('nick \"%s\" not found.','%s/%s'%(jid,nick)) % who
	msg = L('Total conferences: %s, available: %s','%s/%s'%(jid,nick)) % (len(isa)-1, '%s, %s' % (len(djids),msgg))
	send_msg('chat', jid, nick, msg)
	whereis_lock = None

def whereis_collect_async(whereis_id,who,is_answ):
		global whereis_answers
		try:
			result = []
			if is_answ[1][0]:
				names = re.findall(whereis_regx,is_answ[1][0])
				if names:
					conf = get_tag_item(is_answ[1][0],'iq','from')
					for tmp in names:
						if who.lower() in tmp.lower(): result.append([tmp,conf])
			whereis_answers[whereis_id].append(result)
		except: whereis_answers[whereis_id].append([])

global execute, iq_hook

iq_hook = [[100,'get',disco_iq_get],[100,'set',disco_iq_set]]

disco_exclude_update()

execute = [(3, 'disco', disco, 2, 'Service discovery.\ndisco server.tld - request information about server\ndisco conference.server.tld [body [size]] - find body string in conference list and show size results\ndisco room@conference.server.tld [body [size]] - find body string in disco room conference and show size results.'),
	 (3, 'disco_raw', disco_raw, 2, 'Service discovery.\ndisco_raw server.tld - request information about server\ndisco_raw conference.server.tld [body [size]] - find body string in conference list and show size results\ndisco_raw room@conference.server.tld [body [size]] - find body string in disco room conference and show size results.'),
	 (4, 'features', features, 2, 'Show features of object'),
	 (7, 'whereis', whereis, 2, 'Find nick on conference server\nwhereis - find your nick on current conference server\nwhereis nick - find nick on current conference server\nwhereis nick\n[conference.]server.tld - find nick on server server.tld')]
