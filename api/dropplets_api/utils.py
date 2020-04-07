import trafaret as T


# defines exactly all atributes from config/asatra_api-xxx.yaml
TRAFARET = T.Dict({
    T.Key('postgres'):
        T.Dict({
            'databases': T.List(T.String()),
            'user': T.String(),
            'password': T.String(),
            'host': T.String(),
            'port': T.Int(),
            'minsize': T.Int(),
            'maxsize': T.Int(),
        }),
    T.Key('redis'):
        T.Dict({
            'host': T.String(),
            'port': T.Int(),
        }),
    T.Key('host'): T.IP,
    T.Key('port'): T.Int(),
})
