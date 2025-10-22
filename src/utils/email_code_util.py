import smtplib
from  email.message import EmailMessage
from random import choice
from re import match

from dotenv import load_dotenv

from src.core.constraints import Constraints, HttpStatus
from src.exceptions.send_email_exception import SendEmailException
from src.utils.password_util import PasswordUtil
from src.utils.regex import Regex

load_dotenv()


class EmailCodeUtil:
    @classmethod
    async def send_email_verification_code(cls, email_receiver: str) -> str:
        if not match(Regex.EMAIL.value, email_receiver):
            raise SendEmailException("invalid email receiver found", HttpStatus.BAD_REQUEST)

        credentials = await cls._get_envs_email_and_password_()

        if None in credentials.values():
            raise SendEmailException("invalid credentials email or password", HttpStatus.BAD_REQUEST)

        message = EmailMessage()
        message["Subject"] = "Acelera Concurso | Código de Verificação"
        message["From"] = credentials["email"]
        message["To"] = email_receiver

        activation_code = await cls._code_generator_()

        msg_content = (
            "Acelera Concurso\n\nOlá, tudo bem? Você está recebendo esse email com o "
            + "código de verificação de sua conta em nossa plataforma.\n\n"
            + f"O Código de Ativação é: {activation_code}\n\n"
            + "NÃO COMPARTILHE ESSE CÓDIGO COM NINGUÉM!\n\n"
            + "Agora você pode confirmar na nossa plataforma o código fornecido!\n\n"
            + "Acelera Concurso\nUma Iniciativa BCarSoftware"
        )

        message.set_content(msg_content)

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(credentials["email"], credentials["password"])
                smtp.send_message(message)
        except smtplib.SMTPAuthenticationError as a_e:
            print(f"SMTP Authentication Failed. {a_e}")
            raise SendEmailException("SMTP authentication failed", HttpStatus.BAD_REQUEST)
        except smtplib.SMTPConnectError as c_e:
            print(f"Can't connect to SMTP Server. {c_e}")
            raise SendEmailException("can't connect to SMTP server", HttpStatus.BAD_REQUEST)
        except Exception as e:
            print(f"Something went wrong to send email: {e}")
            raise SendEmailException("something went wrong to send email", HttpStatus.BAD_REQUEST)

        return await PasswordUtil.encrypt(activation_code)

    @classmethod
    async def verify_encrypted_verification_code(cls, verification_code: str, secure_code: str) -> None:
        result = await PasswordUtil.verify(verification_code, secure_code)

        if not result:
            raise SendEmailException("verification code doesn't match", HttpStatus.BAD_REQUEST)

    @classmethod
    async def _code_generator_(cls) -> str:
        letters = tuple(chr(_) for _ in range(65, 91))
        numbers = ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0")

        tree_first_letters = "".join(choice(letters) for _ in range(3))
        one_number = choice(numbers)
        one_letter = choice(letters)
        two_numbers = "".join(choice(numbers) for _ in range(2))

        return f"{tree_first_letters}{one_number}{one_letter}{two_numbers}"

    @classmethod
    async def _get_envs_email_and_password_(cls) -> dict[str, str]:
        email = Constraints.EMAIL_ADDRESS
        password = Constraints.EMAIL_PASSWORD

        return { "email": email, "password": password }
