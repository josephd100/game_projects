-- Start with load, update, and draw functions

function love.load()
    -- Create a target table 
    target = {}
    target.x, target.y = 400, 300
    target.radius = 50

    --Create a score and timer
    score = 0
    timer = 0
    gameFont = love.graphics.newFont(40)
    gamestate = 1

    sprites = {}
    sprites.sky = love.graphics.newImage('sprites/sky.png')
    sprites.target = love.graphics.newImage('sprites/target.png')
    sprites.crosshairs = love.graphics.newImage('sprites/crosshairs.png')
    love.mouse.setVisible(false)
end 

function love.update(dt)
    if timer > 0 then 
        timer = timer - dt
    end 

    if timer < 0 then 
        timer = 0
        gamestate = 1
    end 
end 

function love.draw()
    -- mode (fill, line), x, y, width, height
    love.graphics.circle("fill", target.x, target.y, target.radius)
    love.graphics.draw(sprites.sky, 0, 0)
    if gamestate == 2 then 
        love.graphics.draw(sprites.target, target.x - target.radius, target.y - target.radius)
        scoreText = "Score: " .. score
        timerText = "Time: " .. math.ceil(timer)
    end
    if gamestate == 1 then 
        love.graphics.printf("Click anywhere to begin", 0, love.graphics.getHeight() / 2, love.graphics.getWidth(), "center")
    end
    love.graphics.draw(sprites.crosshairs, love.mouse.getX() - 20, love.mouse.getY() - 20)
    love.graphics.setColor(10, 0, 0)
    love.graphics.setFont(gameFont)
    local scoreText = "Score: " .. score
    local timerText = "Time: " .. math.ceil(timer)
    local scoreTextWidth = love.graphics.getFont():getWidth(scoreText)
    love.graphics.setColor(255, 255, 255)
    love.graphics.print(scoreText,(love.graphics.getWidth() / 2) - (scoreTextWidth / 2), 0)
    love.graphics.print(timerText, 0, 0)
end 

function love.mousepressed(x, y, button, istouch, presses)
    if button == 1 and gamestate == 2 then
        local mouseToTarget = distanceBetween(x, y, target.x, target.y) 
        if mouseToTarget < target.radius then 
            score = score + 1
            target.x = math.random(target.radius, love.graphics.getWidth() - target.radius)
            target.y = math.random(target.radius, love.graphics.getHeight() - target.radius)
        end
    elseif button == 1 and gamestate == 1 then 
        gamestate = 2
        timer = 10
        score = 0
    end 
end


function distanceBetween(x1, y1, x2, y2)
   return math.sqrt((x2 - x1)^2 + (y2 - y1)^2)
end 

print(screen_width)
print(screen_height)