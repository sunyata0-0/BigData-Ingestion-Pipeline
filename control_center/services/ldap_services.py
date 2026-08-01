from ldap3 import Server, Connection, ALL


class LDAPService:

    def __init__(
        self,
        server,
        port,
        bind_dn,
        bind_password,
        base_dn,
        admin_password,
        viewer_password
    ):

        self.server = server
        self.port = port
        self.bind_dn = bind_dn
        self.bind_password = bind_password
        self.base_dn = base_dn

        self.admin_password = admin_password
        self.viewer_password = viewer_password


    def _connect(self):
        server = Server(
            self.server,
            port=self.port,
            get_info=ALL
        )

        return Connection(
            server,
            user=self.bind_dn,
            password=self.bind_password,
            auto_bind=True
        )


    def get_users(self):

        try:

            conn = self._connect()

            conn.search(
                search_base=f"ou=people,{self.base_dn}",
                search_filter="(uid=*)",
                attributes=["uid"]
            )

            users = []

            for entry in conn.entries:

                username = str(entry.uid)

                role = (
                    "Administrator"
                    if username == "mahdi"
                    else "Viewer"
                )

                users.append({
                    "username": username,
                    "role": role
                })

            conn.unbind()

            return users

        except Exception:

            return []


    def verify_master_password(self, password):

        return password == self.admin_password


    def get_passwords(self):

        return {
            "mahdi": self.admin_password,
            "viewer": self.viewer_password
        }