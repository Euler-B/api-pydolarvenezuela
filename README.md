# pyDolarVenezuela API

La API de pyDolarVenezuela es una herramienta eficiente y confiable que brinda información en tiempo real sobre el valor del dólar y euro en Venezuela. Además, facilita la conversión precisa entre bolívares y estas monedas extranjeras.

Swagger API: https://pydolarve.org/apidocs

## URL base

```
https://pydolarve.org/
```

## Endpoints

### `GET /`

Este endpoint muestra un mensaje de bienvenida y proporciona un enlace a la documentación de la API.

### `GET /api/v1/<currency>`

Este endpoint permite obtener todas las entidades de seguimiento del dólar y/o euro, junto con su nombre correspondiente, cambio y fecha de la última actualización. Ademas permite obtener información sobre el monitor en una página específica. 

**Las páginas disponibles son**: 

- **Fuentes directas**:

| Página web | Ruta |
| ----  | ---- |
| [<code><img height="50" alt="Banco Central de Venezuela" src="https://github.com/fcoagz/api-pydolarvenezuela/blob/docker/assets/pages/BCV.png?raw=true"></code>](https://www.bcv.org.ve/) | `api/v1/dollar?page=bcv` |
| [<code><img height="50" alt="EnParaleloVzla" src="https://github.com/fcoagz/api-pydolarvenezuela/blob/docker/assets/pages/EnParaleloVzla.png?raw=true"></code>](https://t.me/enparalelovzlatelegram)  | `api/v1/dollar?page=enparalelovzla` |
| [<code><img height="50" alt="Italcambio" src="https://github.com/fcoagz/api-pydolarvenezuela/blob/docker/assets/pages/Italcambio.png?raw=true"></code>](https://www.italcambio.com/) | `api/v1/dollar?page=italcambio`

- **Fuentes informativas**:

| Página web | Ruta |
| ----  | ---- |
| [<code><img height="50" alt="AlCambio" src="https://github.com/fcoagz/api-pydolarvenezuela/blob/docker/assets/pages/AlCambio.png?raw=true"></code>](https://alcambio.app/)  | `api/v1/dollar?page=alcambio` |
| [<code><img height="50" alt="Criptodolar" src="https://github.com/fcoagz/api-pydolarvenezuela/blob/docker/assets/pages/Criptodolar.png?raw=true"></code>](https://criptodolar.net/)  | `api/v1/<currency>?page=criptodolar` |
| [<code><img height="50" alt="Dolartodayn" src="https://github.com/fcoagz/api-pydolarvenezuela/blob/docker/assets/pages/Dolartoday.png?raw=true"></code>](https://dolartoday.com/) | `api/v1/dollar?page=dolartoday` |


Ruta:
- `currency`: La moneda en la que se expresarán los precios (`dollar`, `euro`).

| Parámetros | Tipo | Descripción |
|------------|------|-------------|
| page       | `string` | _Opcional._ Indica el nombre de la página donde deseas obtener su valor. |
| monitor    | `string` | _Opcional._ Indica el monitor específico. |
| format_date    | `string` | _Opcional._ Indica el tipo de formato de fecha. (`iso`, `timestamp`, `default`) |

El parámetro `format_date` permite obtener la fecha en diferentes formatos. Por defecto, la fecha se muestra en formato `DD/MM/YYYY,  HH:mm AM/PM`. Si deseas obtener la fecha en formato `ISO` o `timestamp`, puedes especificarlo en el parámetro `format_date`.

### `GET /api/v1/<currency>/history`

Este endpoint le permite conocer el historial de precios de un monitor especificando la fecha de inicio y finalización.

Ruta:
- `currency`: La moneda en la que se expresarán los precios (`dollar`, `euro`).

Header:
- `Authorization`: El token de autorización correspondiente al usuario.

| Parámetros | Tipo | Descripción |
|------------|------|-------------|
| page       | `string` | Indica el nombre de la página donde deseas obtener su valor. |
| monitor    | `string` | Indica el monitor específico. |
| start_date    | `string` | Fecha de inicio del historial. `DD-MM-YYYY` |
| end_date   | `string` | Fecha de fin del historial. `DD-MM-YYYY` |
| format_date    | `string` | _Opcional._ Indica el tipo de formato de fecha. (`iso`, `timestamp`, `default`) |

### `GET /api/v1/<currency>/changes`

Este endpoint permite conocer los cambios que ha obtenido el monitor en un día concreto. (Actualizaciones de precios)

Ruta:
- `currency`: La moneda en la que se expresarán los precios (`dollar`, `euro`).

Header:
- `Authorization`: El token de autorización correspondiente al usuario.

| Parámetros | Tipo | Descripción |
|------------|------|-------------|
| page       | `string` | Indica el nombre de la página donde deseas obtener su valor. |
| monitor    | `string` | Indica el monitor específico. |
| date    | `string` | Fecha de la cual se desea obtener los precios. `DD-MM-YYYY` |
| format_date    | `string` | _Opcional._ Indica el tipo de formato de fecha. (`iso`, `timestamp`, `default`) |

### `GET /api/v1/<currency>/conversion`

Este endpoint convierte un valor en bolívares a su equivalente a estas monedas extranjeras y viceversa.

Ruta:
- `currency`: La moneda en la que se expresarán los precios (`dollar`, `euro`).

| Parámetros | Tipo | Descripción |
|------------|------|-------------|
| type       | `string` | Indica el tipo de conversión. Puede ser `VES` o `USD` o `EUR`. |
| value      | `float or integer` | Indica el valor a convertir. |
| page       | `string` | Indica el nombre de la página donde deseas obtener su valor. |
| monitor    | `string` | Indica el monitor específico. |

### Webhooks

La API de pyDolarVenezuela también permite configurar webhooks para recibir notificaciones en tiempo real sobre los cambios de precios de los monitores. Para ello, debes proporcionar la URL de tu servidor y el token de autorización correspondiente.

### `GET /api/user/get-webhook`

Este endpoint permite obtener todos los webhooks configurados por el usuario.

Header:
- `Authorization`: El token de autorización correspondiente al usuario.

### `POST /api/user/set-webhook`

Este endpoint permite configurar un webhook para recibir notificaciones en tiempo real sobre los cambios de precios de los monitores.

Header:
- `Authorization`: El token de autorización correspondiente al usuario.

El `token_secret` es una clave secreta que se utilizará para verificar la autenticidad de las solicitudes entrantes. Y sera enviado en el header `Authorization` como `Bearer <token_secret>`.

Body:
```json
{
  "url": "string",
  "certificate_ssl": true,
  "token_secret": "string",
  "monitors": [
    {
      "page": "string",
      "currency": "string", // dollar or euro
      "monitor": "string"
    }
  ]
}
```

> [!NOTE]
> Una vez configurado el webhook, el servidor enviará una solicitud `POST` a la URL proporcionada cada vez que se produzca un cambio, despues de 3 intentos fallidos su estado pasará a `false`.

### `DELETE /api/user/del-webhook`

Este endpoint permite eliminar un webhook configurado previamente.

Header:
- `Authorization`: El token de autorización correspondiente al usuario.

## Actividad

![Alt](https://repobeats.axiom.co/api/embed/7fc602e88410dfba302fe708f14e0e30d059a729.svg "Repobeats analytics image")

## Uso
Para obtener información actualizada sobre el precio del dólar en Venezuela de `EnParaleloVzla`, puedes hacer una solicitud GET a la siguiente URL:
```sh
curl -X GET "https://pydolarve.org/api/v1/dollar?monitor=enparalelovzla"
```

Para obtener información sobre el dólar en una página específica, puedes hacer una solicitud GET a la siguiente URL:
```sh
curl -X GET "https://pydolarve.org/api/v1/dollar?page=bcv"
```

## Sponsors

<a href="https://www.capasiete.com/" target="_blank" title="Capa7, proveedor de servicios web hosting, streaming y servidores, servicios rápidos, confiables, y seguros, 99.9% óptimo, soporte 24/7."><img src="https://github.com/fcoagz/api-pydolarvenezuela/blob/docker/assets/sponsor/capasiete.jpg?raw=true" width="250" height="150"></a>
<a href="https://criptomerkado.com/" target="_blank" title="Somos una plataforma para compra y venta de cripto monedas." ><img src="https://github.com/fcoagz/api-pydolarvenezuela/blob/docker/assets/sponsor/criptomerkado.jpg?raw=true" width="250" height="150"></a>

## Individual Sponsors

| [<img src="https://avatars.githubusercontent.com/u/26844099?v=4" width=115><br><sub>José Gregorio</sub>](https://estacionweb.net/) | [<img src="https://avatars.githubusercontent.com/u/130260543?v=4" width=115><br><sub>Bryan</sub>](https://github.com/braymm) | [<img src="https://avatars.githubusercontent.com/u/18505860?v=4" width=115><br><sub>Victor Noguera</sub>](https://github.com/nvictorme) | 
| :---: | :---: | :---: | 




## Apoya este proyecto

Si deseas conocer características interesantes de la API de por vida, considera hacer una donación o suscribirte a través de [Ko-fi](https://ko-fi.com/fcoagz). Tu apoyo contribuirá al continuo desarrollo del proyecto y al mantenimiento de los servicios en los que está alojado.

| Características | Gratis | Token |
| --------------- | ------ | ------ |
| Solicitudes API | 500/hora | ∞ |
| Historial de precios | No | Sí |
| Webhooks | No | Sí |

Envíame un mensaje privado desde Ko-fi para que pueda proporcionarte el token de acceso.

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/O5O5RFF4T)

## Contributores

<a href="https://github.com/fcoagz/api-pydolarvenezuela/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=fcoagz/api-pydolarvenezuela"/>
</a>
