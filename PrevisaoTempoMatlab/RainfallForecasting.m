%Reading From File
filename = '1_3inputs.csv';
amtInputs = 3;
month = 1;
TrainData = csvread(filename, 1, 1);
%TrainData = TrainData';
[nRows, nColumns] = size(TrainData)

%MLP Configuration
net = feedforwardnet;

net.performFcn = 'mse';
trainData = TrainData(:,1:amtInputs)';
target = TrainData(:,nColumns:nColumns)';


%Dividing data for training
net.divideFcn = 'divideblock'
[trainInd, valInd, testInd] = divideblock(nRows, 0.65,  0.1, 0.25)



%training
net.trainParam.epochs = 100;
net.trainParam.mu = 0.003;
net.trainParam.mu_dec = 0.01;
net.trainParam.mu_inc = 7;
net.trainParam.mu_max = 10^10;
net.trainParam.showWindow=0; %set nntraintool window not to appear

qtdLayers = 10;
netLayers = (1:qtdLayers);

mseVCT = zeros(qtdLayers:1);
mapeVCT = zeros(qtdLayers:1);
for i = 1:qtdLayers
    clear train;

    net.layers{1}.dimensions = netLayers(i);
    net = configure(net,trainData,target);
    [net,tr] = train(net, trainData, target);
    %getting performance parameters
    
    %getting Mean Square Error
    result = net(trainData);
    error = result - target;
    mseVCT(i,1) = mse(error);
    
    %getting Mean Absolute Percentage Error (MAPE)
    [nRowsTD,nCollumnsTD] = size(tr.testInd);
    errorTestData = zeros(2,nRowsTD);
    for j = 1:nRowsTD
        indice = tr.testInd(:,j);
        errorTestData(:,j) = result(:,indice) - target(:,indice);
    end
    
    mapeVCT(i,1) = 100*(mae(errorTestData));
    
end

%display perform parameters
display(mapeVCT);
%display((100 - mapeVCT))
display(mseVCT);
