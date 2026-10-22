# A função de recuperação do código SMS foi fornecida pelo projeto educacional.
# Preserve retrieve_phone_code para manter compatibilidade com esse fluxo.

def retrieve_phone_code(driver) -> str:
    """Este código recupera o número de confirmação do telefone e o retorna como uma string.
    Use-o quando o aplicativo espera o código de confirmação para passá-lo para seus testes.
    O código de confirmação do telefone só pode ser obtido após ser solicitado no aplicativo."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("Nenhum código de confirmação de telefone encontrado.\n"
                            "Use retrieve_phone_code somente depois que o código for solicitado em seu aplicativo.")
        return code

# Verifica se o Routes está ativo e funcionando.
def is_url_reachable(url):
    """Verifique se a URL pode ser acessada. Passe a URL do Urban Routes como parâmetro.
    Se puder ser alcançada, retorna True (verdadeiro), caso contrário, retorna False (falso)"""

    from urllib.error import URLError
    import urllib.request

    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            return response.status == 200
    except (URLError, TimeoutError, ValueError):
        return False

