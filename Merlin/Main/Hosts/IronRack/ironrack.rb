require 'rubygems'
require 'rack'

$LOAD_PATH.unshift APP_ROOT

$app = eval "Rack::Builder.new { #{File.read APP_ROOT + '/config.ru'} }"