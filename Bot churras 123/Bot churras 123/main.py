import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!')

IDs dos cargos
CARGO_1_DIVISAO = 1320752320102793277
CARGO_2_DIVISAO = 1320752372821135411
CARGO_STAFF = 1320752415687053344

Canal para staffs
CANAL_STAFF = 1320752824069525616

@bot.event
async def on_ready():
    print(f'Bot iniciado como {bot.user}')

@bot.command(name='cadastro', help='Solicita cadastro')
async def cadastro(ctx, nome_roblox: str, nome_discord: str, nome_guerra: str, plataforma: str):
    # Verifique se o usuário não é staff
    if ctx.author.roles and any((link unavailable) == CARGO_STAFF for role in ctx.author.roles):
        await ctx.send("Você já é um staff!")
        return

    # Defina os cargos
    cargo_1_divisao = ctx.guild.get_role(CARGO_1_DIVISAO)
    cargo_2_divisao = ctx.guild.get_role(CARGO_2_DIVISAO)

    # Verifique a plataforma
    if plataforma.lower() == 'pc':
        cargo = cargo_1_divisao
    elif plataforma.lower() in ['mobile', 'console']:
        cargo = cargo_2_divisao
    else:
        await ctx.send('Plataforma inválida!')
        return

    # Crie a mensagem de solicitação
    mensagem = f"Solicitação de cadastro:\nNome de Guerra: {nome_guerra}\nPlataforma: {plataforma}\nCargo: {cargo.name}"
    embed = discord.Embed(description=mensagem)
    embed.set_author(name=nome_discord)

    # Envie a mensagem para o canal de staffs
    canal_staff = bot.get_channel(CANAL_STAFF)
    msg = await canal_staff.send(embed=embed)
    await msg.add_reaction('')
    await msg.add_reaction('')

    # Aguarde a reação dos staffs
    def verificar_reacao(reacao, usuario):
        return usuario.roles and any((link unavailable) == CARGO_STAFF for role in usuario.roles) and reacao.emoji in ['', '']

    try:
        reacao, usuario = await bot.wait_for('reaction_add', timeout=300.0, check=verificar_reacao)
    except:
        await ctx.send('Tempo expirado!')
        return

    # Aprovação
    if reacao.emoji == '':
        await ctx.author.add_roles(cargo)
        await ctx.author.edit(nick=nome_guerra)
        await ctx.send(f'Cadastro aprovado! Bem-vindo, {nome_guerra}!')
    # Reprovação
    else:
        await ctx.send(f'Cadastro reprovado por {usuario.name}!')

bot.run('')